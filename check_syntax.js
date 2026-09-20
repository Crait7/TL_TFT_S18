const fs = require("fs");
const html = fs.readFileSync(
  "E:/mimo/projects/.mimo-sessions/2026-09-20/帮我调研现版本云顶之奕棋子的羁绊分布情况，在最多10个棋子+1个花仙子转职的情况/云顶之弈Set18羁绊最优化工具.html",
  "utf8"
);
const start = html.indexOf("<script>");
const end = html.lastIndexOf("</script>");
if (start < 0 || end < 0) {
  console.log("no script tags");
  process.exit(1);
}
const js = html.slice(start + 8, end);
try {
  new Function(js);
  console.log("JS syntax OK, length", js.length);
} catch (e) {
  console.log("SYNTAX ERROR:", e.message);
  process.exit(1);
}
