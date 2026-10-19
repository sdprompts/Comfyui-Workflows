import { app } from "../../scripts/app.js";
import { api } from "../../scripts/api.js";

const TITLE_HEIGHT = 30;
const PAD = 12;
const THUMB_MAX = 180;
const LINE_HEIGHT = 16;

function wrapText(ctx, text, maxWidth) {
	const lines = [];
	for (const paragraph of String(text ?? "").split("\n")) {
		if (!paragraph) {
			lines.push("");
			continue;
		}
		let line = "";
		for (const word of paragraph.split(/\s+/)) {
			let piece = word;
			while (piece && ctx.measureText(piece).width > maxWidth) {
				let cut = piece.length - 1;
				while (cut > 1 && ctx.measureText(piece.slice(0, cut)).width > maxWidth) {
					cut -= 1;
				}
				if (line) {
					lines.push(line);
					line = "";
				}
				lines.push(piece.slice(0, cut));
				piece = piece.slice(cut);
			}
			const next = line ? `${line} ${piece}` : piece;
			if (line && ctx.measureText(next).width > maxWidth) {
				lines.push(line);
				line = piece;
			} else {
				line = next;
			}
		}
		if (line) lines.push(line);
	}
	return lines.length ? lines : [""];
}

function measureContext() {
	const ctx = document.createElement("canvas").getContext("2d");
	ctx.font = "12px sans-serif";
	return ctx;
}

function layoutItems(node, ctx) {
	const width = Math.max(node.size?.[0] || 360, 360);
	const inner = width - PAD * 2;
	let y = TITLE_HEIGHT + PAD;
	const blocks = [];
	for (const item of node.showImageTextItems || []) {
		let thumb = { w: inner, h: 0 };
		if (item.img?.width) {
			const scale = Math.min(inner / item.img.width, THUMB_MAX / item.img.height, 1);
			thumb = { w: item.img.width * scale, h: item.img.height * scale };
		}
		const lines = wrapText(ctx, item.text, inner);
		blocks.push({ item, thumb, lines, y });
		y += (thumb.h ? thumb.h + 8 : 0) + lines.length * LINE_HEIGHT + 14;
	}
	return { width, height: Math.max(y + PAD, 140), blocks };
}

function loadPreviews(node, images, texts) {
	const items = (images || []).map((info, index) => ({
		info,
		text: texts?.[index] ?? "",
		img: null,
	}));
	node.showImageTextItems = items;
	const pending = items.map(
		(item) =>
			new Promise((resolve) => {
				const img = new Image();
				img.onload = () => {
					item.img = img;
					resolve();
				};
				img.onerror = () => resolve();
				const params = new URLSearchParams({
					filename: item.info.filename,
					type: item.info.type || "temp",
					subfolder: item.info.subfolder || "",
				});
				img.src = api.apiURL(`/view?${params}`);
			})
	);
	Promise.all(pending).then(() => {
		const { width, height } = layoutItems(node, measureContext());
		node.setSize([width, height]);
		node.setDirtyCanvas(true, true);
	});
}

app.registerExtension({
	name: "caption_folder.show_image_text",
	async beforeRegisterNodeDef(nodeType, nodeData) {
		const className = nodeData.comfyClass || nodeData.name;
		if (className !== "ShowImageText") return;

		const onExecuted = nodeType.prototype.onExecuted;
		nodeType.prototype.onExecuted = function (message) {
			onExecuted?.apply(this, arguments);
			loadPreviews(this, message?.images || [], message?.text || []);
		};

		const onDrawForeground = nodeType.prototype.onDrawForeground;
		nodeType.prototype.onDrawForeground = function (ctx) {
			onDrawForeground?.apply(this, arguments);
			if (this.flags?.collapsed || !this.showImageTextItems?.length) return;
			const { blocks } = layoutItems(this, ctx);
			ctx.save();
			ctx.font = "12px sans-serif";
			ctx.fillStyle = "#ddd";
			ctx.textBaseline = "top";
			for (const block of blocks) {
				let y = block.y;
				if (block.item.img && block.thumb.h) {
					ctx.drawImage(block.item.img, PAD, y, block.thumb.w, block.thumb.h);
					y += block.thumb.h + 8;
				}
				for (const line of block.lines) {
					ctx.fillText(line, PAD, y);
					y += LINE_HEIGHT;
				}
			}
			ctx.restore();
		};
	},
});
