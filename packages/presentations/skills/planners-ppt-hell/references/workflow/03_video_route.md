# 视频静态关键帧 SVG 导出路线

本工作台与视频风格库、时间轴及动效编排完全解耦。仅在制作 PPT 类视频时使用本路线产出静态关键帧 SVG，完成后交由 `video-craft` 单向读取，无需导出 `.pptx`。

## 静态关键帧 SVG 契约

- **画布尺寸**：默认 1920×1080，根节点统一声明 `width="1920" height="1080" viewBox="0 0 1920 1080" overflow="hidden"`（或沿用项目 `page_manifest.json.canvas`）。
- **干净分层与元素命名**：按视觉语义使用 `<g>` 分层；若下游需元素级控制，可为关键元素附加页内唯一的语义 `id`（推荐 `<page_key>-<role>`），不写死时间轴或动效脚本。
- **样式与资产**：样式内联 `<style>` + `:root` 变量；外部图片路径保持相对可解析且严禁拉伸变形（`preserveAspectRatio="none"`）。

## 保存、检查与导出命名

1. **初始化与制作**：用 `init_svg_project.py <project> --source <上屏稿.md> --route video`（或既有 `--assets` + `--plan`）初始化，经 `workbench_store.py` 走 `checkout → 编辑 → save` 流程。
2. **技术检查**：运行 `ppt_pipeline.py <project> check --summary`，仅执行 SVG 与资产通用校验并渲染 PNG 目检（`DUPLICATE_ELEMENT_ID` 为错误）。
3. **导出与交付命名**：默认按 Store `order` 交付 `get_page` 返回的 `<page_key>.svg`（兼容视图 `_internal/02_svg_source/<page_key>.svg`）及关联素材；如需冻结整套交接版本，运行 `ppt_pipeline.py <project> export` 生成 `snapshot.json`（内含 `scenes/<page_key>.svg`），由 `video-craft` 单向读取。
