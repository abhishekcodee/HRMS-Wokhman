import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import fs from "fs";
import path from "path";

// https://vitejs.dev/config/
export default defineConfig({
	plugins: [vue()],
	server: {
		port: 8081,
		proxy: getProxyOptions(),
		allowedHosts: true,
	},
	resolve: {
		alias: {
			"@": path.resolve(__dirname, "src"),
		},
	},
	build: {
		outDir: `../hrms/public/roster`,
		emptyOutDir: true,
		target: "es2015",
		commonjsOptions: {
			include: [/tailwind.config.js/, /node_modules/],
		},
	},
	optimizeDeps: {
		include: [
			"frappe-ui > feather-icons",
			"showdown",
			"tailwind.config.js",
			"engine.io-client",
		],
	},
});

function getProxyOptions() {
	const config = getCommonSiteConfig();
	const webserver_port = process.env.FRAPPE_PORT || (config ? config.webserver_port : 8005);
	return {
		"^/(app|login|api|assets|files|private)": {
			target: `http://127.0.0.1:${webserver_port}`,
			ws: true,
			changeOrigin: true,
			router: function (req) {
				return `http://127.0.0.1:${webserver_port}`;
			},
		},
	};
}

function getCommonSiteConfig() {
	let currentDir = path.resolve(".");
	let parent = path.resolve(currentDir, "..");
	// traverse up till we find frappe-bench with sites directory
	while (currentDir !== "/" && currentDir !== parent) {
		if (
			fs.existsSync(path.join(currentDir, "sites")) &&
			fs.existsSync(path.join(currentDir, "apps"))
		) {
			let configPath = path.join(currentDir, "sites", "common_site_config.json");
			if (fs.existsSync(configPath)) {
				return JSON.parse(fs.readFileSync(configPath));
			}
			return null;
		}
		currentDir = parent;
		parent = path.resolve(currentDir, "..");
	}
	return null;
}
