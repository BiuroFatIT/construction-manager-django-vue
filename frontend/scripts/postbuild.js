import { copyFileSync, rmSync, mkdirSync, readdirSync, statSync } from "fs";
import { join, resolve } from "path";

// Skrypt zakłada, że startujesz z katalogu frontend!
const distDir = resolve("dist");
const backendTemplates = resolve("../backend/templates");
const backendStatic = resolve("../backend/static");

// 1. Skopiuj index.html do templates
mkdirSync(backendTemplates, { recursive: true });
copyFileSync(join(distDir, "index.html"), join(backendTemplates, "index.html"));

// 2. Skopiuj resztę do static (oprócz index.html)
rmSync(backendStatic, { recursive: true, force: true });
mkdirSync(backendStatic, { recursive: true });

function copyRecursive(srcDir, destDir) {
  readdirSync(srcDir).forEach((item) => {
    const srcPath = join(srcDir, item);
    const destPath = join(destDir, item);
    if (statSync(srcPath).isDirectory()) {
      mkdirSync(destPath, { recursive: true });
      copyRecursive(srcPath, destPath);
    } else if (item !== "index.html") {
      copyFileSync(srcPath, destPath);
    }
  });
}
copyRecursive(distDir, backendStatic);

console.log("✅ Vue build skopiowany do backendu!");
