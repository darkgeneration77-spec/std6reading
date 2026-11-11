# 角马大迁徙 · GitHub Pages 有声电子书

## 使用方法
1. 新建 GitHub public 仓库，把本文件夹**里面**的所有文件（包括 `.github` 隐藏目录）上传到仓库根目录。
2. 仓库 Settings → Pages → Build and deployment → Source 选择 **GitHub Actions**。
3. 打开 Actions，执行 **Build audio reader and deploy Pages**（也会在 main 分支推送后自动执行）。
4. 工作流在 GitHub 云端用 `edge-tts` 生成 23 个普通话女声 MP3、用 `pypinyin` 生成全篇拼音，然后部署网站。学生访问 Pages 链接即可播放。
5. 请先逐句试听并核对拼音、多音字、课文原文。自动配音**不能保证百分百准确**；如需修音，可用自己校对后的 MP3 替换 `audio/001.mp3` 等文件，再重新部署。

## 说明
- 默认语音 `zh-CN-XiaoxiaoNeural`，女声，语速 -10%。
- GitHub Actions 运行期间需要访问在线语音服务，服务变更或限流可能导致生成失败；已经生成的 MP3 可自行保存。
- **当前交付包不含已生成的 MP3**：本地环境无法连接语音服务。GitHub Actions 成功后才会生成并部署。
- 照片转录存在潜在误字；`sentences.json` 是课文源文件，发布前请与原书核对。
- GitHub Pages 网页上的 MP3 可以在 Android Chrome 中播放，不依赖浏览器 TTS。
