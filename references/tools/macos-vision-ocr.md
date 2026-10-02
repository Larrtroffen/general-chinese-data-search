# macos-vision-ocr —— 系统自带中文 OCR（零依赖）

macOS 从 10.15 起自带 Vision 框架（`VNRecognizeTextRequest`），中文（简/繁）+ 英文印刷体识别质量接近商用 OCR，**不需要装任何东西、不上传云端**。这是本机扫描件 OCR 的**首选通道**；只有在需要表格结构 / 公式 LaTeX / 手写（质量不够）时才升级到 GLM-OCR 或 MinerU。

- 去哪找：无需安装（调用系统框架）；参考实现 `jiawood2006/doc-ocr`（MIT，Gitee 上的 hermes 技能，用 `pyobjc-framework-Vision` 调同一套框架 + `pymupdf` 拆 PDF 页）——本库只借鉴思路，不引入其依赖
- 什么时候用：政府/方志/统计年鉴的**扫描图**、图片版 PDF、截图里的中文文字要转文本；台账照片、公文照片、民国报刊影印页（印刷体）；需要**批量、离线、免费、无 key**（不满足再走 `glm-ocr.md`）
- 怎么用：把 6 行 `ocr.swift`（见下）存盘后 `swift ocr.swift 扫描页.png`；图片版 PDF 先拆页再逐页 OCR
- 覆盖：单张位图（PNG/JPG/TIFF/HEIC，`CGImageSource` 支持的都行），PDF 需外部拆页；语言 `["zh-Hans","zh-Hant","en-US","ja-JP","ko-KR"]` 等，中英混排建议 `["zh-Hans","en-US"]`；印刷体/清晰手写好，潦草手写、竖排古籍、印章、超小字号不保证；表格**只出行文本、不还原单元格结构**；性能单页 ~0.2–0.5 s（Apple Silicon）
- 门槛：仅 macOS；无需 npm/pip/brew、无需联网（首次调用需系统模型校验）
- 实测：2026-10-02，macOS 27.0 (arm64)、Swift 6.4，`swift ocr.swift /tmp/zh_test.png` → 0.47 s 返回三行正确文本；另一张含公文标题、发文字号「海政发〔2024〕15号」、日期的测试图也正确识别（仅漏一个「的」）
- 上游：https://github.com/jiawood2006/doc-ocr

## 细节

### 最小可复现（6 行 `ocr.swift`）

把下面 6 行存成 `ocr.swift`，**无需 npm/pip/brew**：

```swift
import Foundation
import Vision
let handler = VNImageRequestHandler(url: URL(fileURLWithPath: CommandLine.arguments[1]))
let req = VNRecognizeTextRequest()
req.recognitionLanguages = ["zh-Hans", "en-US"]   // 繁体用 zh-Hant
req.recognitionLevel = .accurate                  // .fast 更快、精度略低
try handler.perform([req])
print((req.results ?? []).compactMap { $0.topCandidates(1).first?.string }.joined(separator: "\n"))
```

```bash
swift ocr.swift 扫描页.png                 # 单图 → 文本（stdout）
swift ocr.swift 扫描页.png > 页.txt        # 落盘
# 图片版 PDF：先拆页再逐页 OCR（本机无 pdftoppm 时可用 sips/预览，或装 pymupdf：
#   python3 -c "import fitz;d=fitz.open('a.pdf');[d[i].get_pixmap(dpi=300).save(f'/tmp/p{i}.png') for i in range(len(d))]"
#   然后 for f in /tmp/p*.png; do swift ocr.swift "$f"; done ）
```

### 定位精确到行（需要还原版式/表格时）

`req.results` 每项是 `VNRecognizedTextObservation`，用 `$0.boundingBox`（归一化坐标，原点左下）取行框；`topCandidates(1)` 取该行最佳候选，`topCandidates(3)` 可做多候选纠错。

### 覆盖与限制

- 表格**只出行文本、不还原单元格结构**，要结构走 GLM-OCR/MinerU。
- 平台仅 macOS；Linux/Windows 用 PaddleOCR/tesseract 或走 GLM-OCR。
- 许可：调用系统框架，无第三方许可约束。

### 实测记录（2026-10-02）

macOS 27.0 (arm64)、Swift 6.4，`swift ocr.swift /tmp/zh_test.png`（900×260 本机渲染的中文测试图「上海市地方志办公室 / 2024年上海年鉴编纂说明 / 本次共收录条目 1234 条」）→ 0.47 s 返回三行正确文本；另一张含公文标题、发文字号「海政发〔2024〕15号」、日期的测试图也正确识别（仅漏一个「的」）。

## 坑

1. 直接 `swift ocr.swift` **每次都要编译**（首次 ~1 s），批量时先 `swiftc -O ocr.swift -o ocr` 出二进制再循环调用，快很多。
2. `VNImageRequestHandler(url:)` 只能读图片；给 PDF 会静默失败 → 先转图。
3. 首次调用会触发系统模型下载/校验，**离线首次运行可能失败**，之后再离线可用。
4. 输出是**按行拼接**，无标点修复、无段落合并；换行即视觉行，表格会串行。长文后续要做后处理（去空行、合并短行）。
5. 想连行框一起存，别用 `joined`，直接 dump `boundingBox`（CGRect → `x,y,w,h` 归一化）。
