PS C:\Users\kevin\Documents\University of Otago\COSC345\Group_11> pylint .
************* Module app
app.py:38:7: W0718: Catching too general exception Exception (broad-exception-caught)
app.py:42:0: C0115: Missing class docstring (missing-class-docstring)
app.py:42:0: R0902: Too many instance attributes (18/7) (too-many-instance-attributes)
app.py:164:28: W0613: Unused argument 'event' (unused-argument)
app.py:170:4: C0116: Missing function or method docstring (missing-function-docstring)
app.py:178:4: C0116: Missing function or method docstring (missing-function-docstring)
app.py:219:4: C0116: Missing function or method docstring (missing-function-docstring)
app.py:253:4: C0116: Missing function or method docstring (missing-function-docstring)
app.py:275:4: C0116: Missing function or method docstring (missing-function-docstring)
app.py:266:8: W0201: Attribute 'prev_viewer' defined outside __init__ (attribute-defined-outside-init)
app.py:276:8: W0201: Attribute 'prev_viewer' defined outside __init__ (attribute-defined-outside-init)
app.py:279:8: W0201: Attribute 'single_viewer' defined outside __init__ (attribute-defined-outside-init)
app.py:308:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:313:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:327:4: W0621: Redefining name 'splash' from outer scope (line 365) (redefined-outer-name)
app.py:332:4: C0103: Variable name "W" doesn't conform to snake_case naming style (invalid-name)
app.py:332:7: C0103: Variable name "H" doesn't conform to snake_case naming style (invalid-name)
app.py:348:11: W0718: Catching too general exception Exception (broad-exception-caught)
app.py:343:40: E1101: Module 'PIL.Image' has no 'LANCZOS' member (no-member)
app.py:371:15: W0718: Catching too general exception Exception (broad-exception-caught)
app.py:31:0: C0411: standard import "tkinter" should be placed before third party import "ttkbootstrap" and first party imports "gui.Sidebar", "db.Database", "photo_importer.PhotoImporter" (...) "sidebar_buttons.SidebarButtons", "scrollable_frame.ScrollableFrame", "faces_frame.FacesFrame"  (wrong-import-order)
************* Module base_sidebar_viewer
base_sidebar_viewer.py:2:0: C0301: Line too long (109/100) (line-too-long)
base_sidebar_viewer.py:13:0: R0901: Too many ancestors (8/7) (too-many-ancestors)
base_sidebar_viewer.py:13:0: R0902: Too many instance attributes (12/7) (too-many-instance-attributes)
base_sidebar_viewer.py:96:4: C0116: Missing function or method docstring (missing-function-docstring)
base_sidebar_viewer.py:112:28: W0613: Unused argument 'event' (unused-argument)
base_sidebar_viewer.py:118:25: W0613: Unused argument 'event' (unused-argument)
base_sidebar_viewer.py:126:4: C0116: Missing function or method docstring (missing-function-docstring)
base_sidebar_viewer.py:113:8: W0201: Attribute '_start_y' defined outside __init__ (attribute-defined-outside-init)
base_sidebar_viewer.py:114:8: W0201: Attribute '_start_height' defined outside __init__ (attribute-defined-outside-init)
************* Module base_viewer
base_viewer.py:1:0: C0114: Missing module docstring (missing-module-docstring)
base_viewer.py:8:0: R0901: Too many ancestors (8/7) (too-many-ancestors)
base_viewer.py:42:35: E1101: Module 'rawpy' has no 'ThumbFormat' member (no-member)
base_viewer.py:43:20: C0415: Import outside toplevel (io.BytesIO) (import-outside-toplevel)
base_viewer.py:75:15: W0718: Catching too general exception Exception (broad-exception-caught)
base_viewer.py:64:45: E1101: Module 'PIL.Image' has no 'LANCZOS' member (no-member)
base_viewer.py:86:15: W0718: Catching too general exception Exception (broad-exception-caught)
base_viewer.py:90:4: C0116: Missing function or method docstring (missing-function-docstring)
base_viewer.py:4:0: C0411: standard import "os" should be placed before third party imports "ttkbootstrap", "PIL.Image" (wrong-import-order)
************* Module collections_viewer
collections_viewer.py:1:0: C0114: Missing module docstring (missing-module-docstring)
collections_viewer.py:12:0: R0901: Too many ancestors (9/7) (too-many-ancestors)
collections_viewer.py:12:0: R0902: Too many instance attributes (10/7) (too-many-instance-attributes)
collections_viewer.py:67:15: W0718: Catching too general exception Exception (broad-exception-caught)
collections_viewer.py:92:15: W0718: Catching too general exception Exception (broad-exception-caught)
collections_viewer.py:107:8: W0706: The except handler raises immediately (try-except-raise)
collections_viewer.py:150:23: W0718: Catching too general exception Exception (broad-exception-caught)
collections_viewer.py:175:4: C0116: Missing function or method docstring (missing-function-docstring)
collections_viewer.py:177:8: W0107: Unnecessary pass statement (unnecessary-pass)
collections_viewer.py:176:8: W0612: Unused variable 'llm_frame' (unused-variable)
collections_viewer.py:122:12: E0203: Access to member 'collections_row' before its definition line 124 (access-member-before-definition)
************* Module db
db.py:190:0: C0301: Line too long (114/100) (line-too-long)
db.py:195:0: C0301: Line too long (101/100) (line-too-long)
db.py:1:0: C0114: Missing module docstring (missing-module-docstring)
db.py:11:0: C0116: Missing function or method docstring (missing-function-docstring)
db.py:13:28: W0212: Access to a protected member _MEIPASS of a client class (protected-access)
db.py:17:0: C0115: Missing class docstring (missing-class-docstring)
db.py:53:4: C0116: Missing function or method docstring (missing-function-docstring)
db.py:58:4: C0116: Missing function or method docstring (missing-function-docstring)
db.py:67:13: W1514: Using open without explicitly specifying an encoding (unspecified-encoding)
db.py:73:4: C0116: Missing function or method docstring (missing-function-docstring)
db.py:77:4: C0116: Missing function or method docstring (missing-function-docstring)
db.py:80:4: C0116: Missing function or method docstring (missing-function-docstring)
db.py:80:29: W0613: Unused argument 'collection_id' (unused-argument)
db.py:81:8: W0612: Unused variable 'query' (unused-variable)
db.py:88:4: C0116: Missing function or method docstring (missing-function-docstring)
db.py:105:4: C0116: Missing function or method docstring (missing-function-docstring)
db.py:126:4: C0116: Missing function or method docstring (missing-function-docstring)
db.py:133:4: C0116: Missing function or method docstring (missing-function-docstring)
db.py:142:4: C0116: Missing function or method docstring (missing-function-docstring)
db.py:149:4: C0116: Missing function or method docstring (missing-function-docstring)
db.py:160:4: C0116: Missing function or method docstring (missing-function-docstring)
db.py:166:4: C0116: Missing function or method docstring (missing-function-docstring)
db.py:170:4: C0116: Missing function or method docstring (missing-function-docstring)
db.py:173:4: C0116: Missing function or method docstring (missing-function-docstring)
db.py:176:4: C0116: Missing function or method docstring (missing-function-docstring)
db.py:180:4: C0116: Missing function or method docstring (missing-function-docstring)
db.py:189:4: C0116: Missing function or method docstring (missing-function-docstring)
db.py:194:4: C0116: Missing function or method docstring (missing-function-docstring)
db.py:198:4: C0116: Missing function or method docstring (missing-function-docstring)
db.py:223:15: W0718: Catching too general exception Exception (broad-exception-caught)
db.py:246:15: W0718: Catching too general exception Exception (broad-exception-caught)
db.py:325:4: C0116: Missing function or method docstring (missing-function-docstring)
db.py:17:0: R0904: Too many public methods (39/20) (too-many-public-methods)
************* Module duplicates
duplicates.py:100:0: C0301: Line too long (101/100) (line-too-long)
duplicates.py:17:5: W0511: TODO: Find better threshold value (fixme)
duplicates.py:1:0: C0114: Missing module docstring (missing-module-docstring)
duplicates.py:4:0: C0413: Import "from PIL import Image" should be placed at the top of the module (wrong-import-position)
duplicates.py:5:0: C0413: Import "import imagehash" should be placed at the top of the module (wrong-import-position)
duplicates.py:6:0: C0413: Import "import numpy as np" should be placed at the top of the module (wrong-import-position)
duplicates.py:7:0: C0413: Import "from sklearn.cluster import DBSCAN" should be placed at the top of the module (wrong-import-position)
duplicates.py:8:0: C0413: Import "from db import Database" should be placed at the top of the module (wrong-import-position)
duplicates.py:30:4: R0914: Too many local variables (21/15) (too-many-locals)
duplicates.py:54:19: W0718: Catching too general exception Exception (broad-exception-caught)
duplicates.py:105:19: W0718: Catching too general exception Exception (broad-exception-caught)
duplicates.py:69:8: R1702: Too many nested blocks (6/5) (too-many-nested-blocks)
duplicates.py:30:4: R0912: Too many branches (15/12) (too-many-branches)
duplicates.py:11:0: R0903: Too few public methods (1/2) (too-few-public-methods)
************* Module duplicate_viewer
duplicate_viewer.py:1:0: C0114: Missing module docstring (missing-module-docstring)
duplicate_viewer.py:4:0: C0115: Missing class docstring (missing-class-docstring)
duplicate_viewer.py:4:0: R0901: Too many ancestors (9/7) (too-many-ancestors)
************* Module exif_reader
exif_reader.py:1:0: C0114: Missing module docstring (missing-module-docstring)
exif_reader.py:17:4: C0116: Missing function or method docstring (missing-function-docstring)
exif_reader.py:17:4: R0914: Too many local variables (19/15) (too-many-locals)
exif_reader.py:57:15: W0718: Catching too general exception Exception (broad-exception-caught)
exif_reader.py:40:23: W0718: Catching too general exception Exception (broad-exception-caught)
exif_reader.py:10:0: R0903: Too few public methods (1/2) (too-few-public-methods)
exif_reader.py:5:0: C0411: standard import "os" should be placed before third party imports "PIL.Image", "piexif" (wrong-import-order)
exif_reader.py:6:0: W0611: Unused import rawpy (unused-import)
************* Module exif_viewer
exif_viewer.py:1:0: C0114: Missing module docstring (missing-module-docstring)
exif_viewer.py:4:0: C0115: Missing class docstring (missing-class-docstring)
exif_viewer.py:4:0: R0901: Too many ancestors (9/7) (too-many-ancestors)
************* Module faces_frame
faces_frame.py:11:0: C0301: Line too long (111/100) (line-too-long)
faces_frame.py:1:0: C0114: Missing module docstring (missing-module-docstring)
************* Module face_frame
face_frame.py:1:0: C0114: Missing module docstring (missing-module-docstring)
************* Module filmstrip_viewer
filmstrip_viewer.py:1:0: C0114: Missing module docstring (missing-module-docstring)
filmstrip_viewer.py:8:0: R0901: Too many ancestors (9/7) (too-many-ancestors)
filmstrip_viewer.py:8:0: R0902: Too many instance attributes (9/7) (too-many-instance-attributes)
filmstrip_viewer.py:14:4: R0913: Too many arguments (6/5) (too-many-arguments)
filmstrip_viewer.py:14:4: R0917: Too many positional arguments (6/5) (too-many-positional-arguments)
filmstrip_viewer.py:85:4: C0116: Missing function or method docstring (missing-function-docstring)
filmstrip_viewer.py:101:12: W0212: Access to a protected member _on_photo_click of a client class (protected-access)
filmstrip_viewer.py:110:16: W0212: Access to a protected member _show_single_photo of a client class (protected-access)
************* Module gui
gui.py:1:0: C0114: Missing module docstring (missing-module-docstring)
gui.py:11:0: C0115: Missing class docstring (missing-class-docstring)
gui.py:11:0: R0901: Too many ancestors (8/7) (too-many-ancestors)
gui.py:11:0: R0902: Too many instance attributes (11/7) (too-many-instance-attributes)
gui.py:12:4: R0913: Too many arguments (7/5) (too-many-arguments)
gui.py:12:4: R0917: Too many positional arguments (7/5) (too-many-positional-arguments)
gui.py:17:8: W0613: Unused argument 'db' (unused-argument)
gui.py:18:8: W0613: Unused argument 'photo_viewer' (unused-argument)
gui.py:19:8: W0613: Unused argument 'importer' (unused-argument)
gui.py:65:4: C0116: Missing function or method docstring (missing-function-docstring)
gui.py:75:28: W0613: Unused argument 'event' (unused-argument)
gui.py:81:25: W0613: Unused argument 'event' (unused-argument)
gui.py:76:8: W0201: Attribute '_start_x' defined outside __init__ (attribute-defined-outside-init)
gui.py:77:8: W0201: Attribute '_start_width' defined outside __init__ (attribute-defined-outside-init)
gui.py:3:0: W0611: Unused SidebarButtons imported from sidebar_buttons (unused-import)
************* Module llm_feedback
llm_feedback.py:42:0: C0301: Line too long (125/100) (line-too-long)
llm_feedback.py:42:0: C0301: Line too long (125/100) (line-too-long)
llm_feedback.py:1:0: C0114: Missing module docstring (missing-module-docstring)
llm_feedback.py:14:0: C0115: Missing class docstring (missing-class-docstring)
llm_feedback.py:48:4: C0415: Import outside toplevel (json) (import-outside-toplevel)
************* Module main_viewer
main_viewer.py:1:0: C0114: Missing module docstring (missing-module-docstring)
main_viewer.py:5:0: R0901: Too many ancestors (8/7) (too-many-ancestors)
main_viewer.py:36:34: W0613: Unused argument 'event' (unused-argument)
main_viewer.py:41:25: W0613: Unused argument 'event' (unused-argument)
main_viewer.py:53:8: W0107: Unnecessary pass statement (unnecessary-pass)
************* Module photo_analyzer
photo_analyzer.py:1:0: C0114: Missing module docstring (missing-module-docstring)
photo_analyzer.py:70:19: W0718: Catching too general exception Exception (broad-exception-caught)
photo_analyzer.py:82:8: C0415: Import outside toplevel (sklearn.cluster.DBSCAN) (import-outside-toplevel)
************* Module photo_importer
photo_importer.py:1:0: C0114: Missing module docstring (missing-module-docstring)
photo_importer.py:10:0: C0115: Missing class docstring (missing-class-docstring)
photo_importer.py:33:4: C0116: Missing function or method docstring (missing-function-docstring)
photo_importer.py:41:19: W0718: Catching too general exception Exception (broad-exception-caught)
photo_importer.py:46:4: C0116: Missing function or method docstring (missing-function-docstring)
photo_importer.py:88:15: W0718: Catching too general exception Exception (broad-exception-caught)
************* Module photo_scorer
photo_scorer.py:1:0: C0114: Missing module docstring (missing-module-docstring)
photo_scorer.py:19:4: R0914: Too many local variables (18/15) (too-many-locals)
photo_scorer.py:25:8: C0415: Import outside toplevel (os) (import-outside-toplevel)
photo_scorer.py:49:19: W0718: Catching too general exception Exception (broad-exception-caught)
photo_scorer.py:44:39: E1101: Module 'rawpy' has no 'ThumbFormat' member (no-member)
photo_scorer.py:46:30: E1101: Module 'cv2' has no 'imdecode' member (no-member)
photo_scorer.py:46:54: E1101: Module 'cv2' has no 'IMREAD_COLOR' member (no-member)
photo_scorer.py:52:18: E1101: Module 'cv2' has no 'imread' member (no-member)
photo_scorer.py:56:15: E1101: Module 'cv2' has no 'cvtColor' member (no-member)
photo_scorer.py:56:33: E1101: Module 'cv2' has no 'COLOR_BGR2GRAY' member (no-member)
photo_scorer.py:57:14: E1101: Module 'cv2' has no 'cvtColor' member (no-member)
photo_scorer.py:57:32: E1101: Module 'cv2' has no 'COLOR_BGR2HSV' member (no-member)
photo_scorer.py:65:19: E1101: Module 'cv2' has no 'resize' member (no-member)
photo_scorer.py:65:60: E1101: Module 'cv2' has no 'INTER_AREA' member (no-member)
photo_scorer.py:66:18: E1101: Module 'cv2' has no 'resize' member (no-member)
photo_scorer.py:66:58: E1101: Module 'cv2' has no 'INTER_AREA' member (no-member)
photo_scorer.py:67:18: E1101: Module 'cv2' has no 'resize' member (no-member)
photo_scorer.py:67:58: E1101: Module 'cv2' has no 'INTER_AREA' member (no-member)
photo_scorer.py:71:35: E1101: Module 'cv2' has no 'Laplacian' member (no-member)
photo_scorer.py:71:55: E1101: Module 'cv2' has no 'CV_64F' member (no-member)
photo_scorer.py:73:33: E1101: Module 'cv2' has no 'Sobel' member (no-member)
photo_scorer.py:73:49: E1101: Module 'cv2' has no 'CV_64F' member (no-member)
photo_scorer.py:74:35: E1101: Module 'cv2' has no 'Sobel' member (no-member)
photo_scorer.py:74:51: E1101: Module 'cv2' has no 'CV_64F' member (no-member)
photo_scorer.py:77:49: E1101: Module 'cv2' has no 'GaussianBlur' member (no-member)
photo_scorer.py:183:8: W0612: Unused variable 'overall_quality' (unused-variable)
photo_scorer.py:224:9: C0103: Variable name "B" doesn't conform to snake_case naming style (invalid-name)
photo_scorer.py:224:12: C0103: Variable name "G" doesn't conform to snake_case naming style (invalid-name)
photo_scorer.py:224:15: C0103: Variable name "R" doesn't conform to snake_case naming style (invalid-name)
photo_scorer.py:224:20: E1101: Module 'cv2' has no 'split' member (no-member)
photo_scorer.py:235:15: E1101: Module 'cv2' has no 'calcHist' member (no-member)
photo_scorer.py:247:19: E1101: Module 'cv2' has no 'imread' member (no-member)
photo_scorer.py:252:23: E1101: Module 'cv2' has no 'CascadeClassifier' member (no-member)
photo_scorer.py:257:15: E1101: Module 'cv2' has no 'cvtColor' member (no-member)
photo_scorer.py:257:38: E1101: Module 'cv2' has no 'COLOR_BGR2GRAY' member (no-member)
photo_scorer.py:6:0: C0411: third party import "rawpy" should be placed before first party import "db.Database"  (wrong-import-order)
photo_scorer.py:7:0: C0411: standard import "io.BytesIO" should be placed before third party imports "cv2", "numpy", "skimage.filters", "rawpy" and first party import "db.Database"  (wrong-import-order)
photo_scorer.py:4:0: W0611: Unused filters imported from skimage (unused-import)
photo_scorer.py:7:0: W0611: Unused BytesIO imported from io (unused-import)
************* Module photo_viewer
photo_viewer.py:1:0: C0114: Missing module docstring (missing-module-docstring)
photo_viewer.py:14:0: R0901: Too many ancestors (10/7) (too-many-ancestors)
photo_viewer.py:14:0: R0902: Too many instance attributes (23/7) (too-many-instance-attributes)
photo_viewer.py:102:4: C0116: Missing function or method docstring (missing-function-docstring)
photo_viewer.py:105:15: W0718: Catching too general exception Exception (broad-exception-caught)
photo_viewer.py:114:4: C0116: Missing function or method docstring (missing-function-docstring)
photo_viewer.py:114:4: R0914: Too many local variables (18/15) (too-many-locals)
photo_viewer.py:119:19: W0718: Catching too general exception Exception (broad-exception-caught)
photo_viewer.py:193:12: W0212: Access to a protected member _image_label of a client class (protected-access)
photo_viewer.py:114:4: R0912: Too many branches (13/12) (too-many-branches)
photo_viewer.py:114:4: R0915: Too many statements (55/50) (too-many-statements)
photo_viewer.py:221:49: W0212: Access to a protected member _image_label of a client class (protected-access)
photo_viewer.py:222:16: W0212: Access to a protected member _image_label of a client class (protected-access)
photo_viewer.py:227:48: W0212: Access to a protected member _image_label of a client class (protected-access)
photo_viewer.py:228:12: W0212: Access to a protected member _image_label of a client class (protected-access)
photo_viewer.py:267:23: W0718: Catching too general exception Exception (broad-exception-caught)
photo_viewer.py:307:8: W0212: Access to a protected member _photo_id of a client class (protected-access)
photo_viewer.py:332:15: W0718: Catching too general exception Exception (broad-exception-caught)
photo_viewer.py:349:19: W0718: Catching too general exception Exception (broad-exception-caught)
photo_viewer.py:356:19: W0718: Catching too general exception Exception (broad-exception-caught)
photo_viewer.py:361:4: C0116: Missing function or method docstring (missing-function-docstring)
photo_viewer.py:383:19: W0718: Catching too general exception Exception (broad-exception-caught)
photo_viewer.py:3:0: C0411: standard import "tkinter" should be placed before third party import "ttkbootstrap" (wrong-import-order)
photo_viewer.py:4:0: C0411: standard import "tkinter.scrolledtext.ScrolledText" should be placed before third party import "ttkbootstrap" (wrong-import-order)
photo_viewer.py:5:0: C0411: standard import "tkinter.messagebox" should be placed before third party import "ttkbootstrap" (wrong-import-order)
photo_viewer.py:8:0: C0411: third party import "PIL.Image" should be placed before first party imports "main_viewer.MainViewer", "base_viewer.BaseThumbnailViewer"  (wrong-import-order)
photo_viewer.py:11:0: C0411: standard import "threading" should be placed before third party imports "ttkbootstrap", "PIL.Image" and first party imports "main_viewer.MainViewer", "base_viewer.BaseThumbnailViewer", "photo_analyzer.PhotoAnalyzer", "llm_feedback.make_paragraph"  (wrong-import-order)
photo_viewer.py:8:0: W0611: Unused Image imported from PIL (unused-import)
************* Module progress_dialog
progress_dialog.py:1:0: C0114: Missing module docstring (missing-module-docstring)
progress_dialog.py:6:0: C0115: Missing class docstring (missing-class-docstring)
progress_dialog.py:7:4: R0913: Too many arguments (6/5) (too-many-arguments)
progress_dialog.py:7:4: R0917: Too many positional arguments (6/5) (too-many-positional-arguments)
progress_dialog.py:42:19: W0718: Catching too general exception Exception (broad-exception-caught)
progress_dialog.py:59:15: W0718: Catching too general exception Exception (broad-exception-caught)
progress_dialog.py:70:15: W0718: Catching too general exception Exception (broad-exception-caught)
progress_dialog.py:83:15: W0718: Catching too general exception Exception (broad-exception-caught)
progress_dialog.py:91:15: W0718: Catching too general exception Exception (broad-exception-caught)
progress_dialog.py:131:15: W0718: Catching too general exception Exception (broad-exception-caught)
progress_dialog.py:105:19: W0718: Catching too general exception Exception (broad-exception-caught)
progress_dialog.py:112:23: W0718: Catching too general exception Exception (broad-exception-caught)
progress_dialog.py:120:23: W0718: Catching too general exception Exception (broad-exception-caught)
progress_dialog.py:126:23: W0718: Catching too general exception Exception (broad-exception-caught)
progress_dialog.py:135:19: W0718: Catching too general exception Exception (broad-exception-caught)
progress_dialog.py:3:0: C0411: standard import "tkinter" should be placed before third party import "ttkbootstrap" (wrong-import-order)
************* Module score_viewer
score_viewer.py:1:0: C0114: Missing module docstring (missing-module-docstring)
score_viewer.py:4:0: C0115: Missing class docstring (missing-class-docstring)
score_viewer.py:4:0: R0901: Too many ancestors (9/7) (too-many-ancestors)
************* Module scrollable_frame
scrollable_frame.py:1:0: C0114: Missing module docstring (missing-module-docstring)
scrollable_frame.py:6:0: R0901: Too many ancestors (8/7) (too-many-ancestors)
************* Module sidebar_buttons
sidebar_buttons.py:50:0: C0301: Line too long (106/100) (line-too-long)
sidebar_buttons.py:68:0: C0301: Line too long (114/100) (line-too-long)
sidebar_buttons.py:292:0: C0301: Line too long (102/100) (line-too-long)
sidebar_buttons.py:302:0: C0301: Line too long (107/100) (line-too-long)
sidebar_buttons.py:310:0: C0301: Line too long (109/100) (line-too-long)
sidebar_buttons.py:1:0: C0114: Missing module docstring (missing-module-docstring)
sidebar_buttons.py:4:0: C0410: Multiple imports on one line (shutil, uuid) (multiple-imports)
sidebar_buttons.py:11:0: R0902: Too many instance attributes (8/7) (too-many-instance-attributes)
sidebar_buttons.py:31:4: C0116: Missing function or method docstring (missing-function-docstring)
sidebar_buttons.py:38:4: C0116: Missing function or method docstring (missing-function-docstring)
sidebar_buttons.py:39:8: C0415: Import outside toplevel (tkinter) (import-outside-toplevel)
sidebar_buttons.py:129:15: W0718: Catching too general exception Exception (broad-exception-caught)
sidebar_buttons.py:124:23: W0718: Catching too general exception Exception (broad-exception-caught)
sidebar_buttons.py:133:4: C0116: Missing function or method docstring (missing-function-docstring)
sidebar_buttons.py:181:15: W0718: Catching too general exception Exception (broad-exception-caught)
sidebar_buttons.py:168:23: W0718: Catching too general exception Exception (broad-exception-caught)
sidebar_buttons.py:253:19: W0718: Catching too general exception Exception (broad-exception-caught)
sidebar_buttons.py:258:15: W0718: Catching too general exception Exception (broad-exception-caught)
sidebar_buttons.py:261:19: W0718: Catching too general exception Exception (broad-exception-caught)
sidebar_buttons.py:370:15: W0718: Catching too general exception Exception (broad-exception-caught)
sidebar_buttons.py:358:23: W0718: Catching too general exception Exception (broad-exception-caught)
sidebar_buttons.py:290:12: R0912: Too many branches (13/12) (too-many-branches)
sidebar_buttons.py:316:24: W0612: Unused variable 'group_id' (unused-variable)
************* Module single_photo_viewer
single_photo_viewer.py:1:0: C0114: Missing module docstring (missing-module-docstring)
single_photo_viewer.py:10:0: R0901: Too many ancestors (9/7) (too-many-ancestors)
single_photo_viewer.py:10:0: R0902: Too many instance attributes (11/7) (too-many-instance-attributes)
single_photo_viewer.py:29:15: W0718: Catching too general exception Exception (broad-exception-caught)
single_photo_viewer.py:33:15: W0718: Catching too general exception Exception (broad-exception-caught)
single_photo_viewer.py:103:15: W0718: Catching too general exception Exception (broad-exception-caught)
single_photo_viewer.py:112:15: W0718: Catching too general exception Exception (broad-exception-caught)
single_photo_viewer.py:125:60: E1101: Module 'PIL.Image' has no 'LANCZOS' member (no-member)
single_photo_viewer.py:145:15: W0718: Catching too general exception Exception (broad-exception-caught)
single_photo_viewer.py:174:19: W0718: Catching too general exception Exception (broad-exception-caught)
single_photo_viewer.py:182:19: W0718: Catching too general exception Exception (broad-exception-caught)
single_photo_viewer.py:216:19: W0718: Catching too general exception Exception (broad-exception-caught)
single_photo_viewer.py:201:8: W0612: Unused variable 'collection_id' (unused-variable)
single_photo_viewer.py:5:0: C0411: standard import "tkinter.scrolledtext.ScrolledText" should be placed before third party imports "ttkbootstrap", "PIL.Image" and first party import "main_viewer.MainViewer"  (wrong-import-order)
single_photo_viewer.py:7:0: C0411: standard import "threading" should be placed before third party imports "ttkbootstrap", "PIL.Image" and first party imports "main_viewer.MainViewer", "llm_feedback.make_paragraph"  (wrong-import-order)
************* Module Design.PrototypeGUI.gui-test
Design\PrototypeGUI\gui-test.py:1:0: C0103: Module name "gui-test" doesn't conform to snake_case naming style (invalid-name)
************* Module Design.Prototypes.Daniel.Prototype Image Analyisis.img-anal
Design\Prototypes\Daniel\Prototype Image Analyisis\img-anal.py:1:0: C0114: Missing module docstring (missing-module-docstring)
Design\Prototypes\Daniel\Prototype Image Analyisis\img-anal.py:1:0: C0103: Module name "img-anal" doesn't conform to snake_case naming style (invalid-name)
Design\Prototypes\Daniel\Prototype Image Analyisis\img-anal.py:11:11: E1101: Module 'cv2' has no 'cvtColor' member (no-member)
Design\Prototypes\Daniel\Prototype Image Analyisis\img-anal.py:11:30: E1101: Module 'cv2' has no 'COLOR_BGR2GRAY' member (no-member)
Design\Prototypes\Daniel\Prototype Image Analyisis\img-anal.py:12:16: E1101: Module 'cv2' has no 'Laplacian' member (no-member)
Design\Prototypes\Daniel\Prototype Image Analyisis\img-anal.py:12:35: E1101: Module 'cv2' has no 'CV_64F' member (no-member)
Design\Prototypes\Daniel\Prototype Image Analyisis\img-anal.py:14:21: E1101: Module 'cv2' has no 'normalize' member (no-member)
Design\Prototypes\Daniel\Prototype Image Analyisis\img-anal.py:14:61: E1101: Module 'cv2' has no 'NORM_MINMAX' member (no-member)
Design\Prototypes\Daniel\Prototype Image Analyisis\img-anal.py:16:11: E1101: Module 'cv2' has no 'GaussianBlur' member (no-member)
Design\Prototypes\Daniel\Prototype Image Analyisis\img-anal.py:17:11: E1101: Module 'cv2' has no 'threshold' member (no-member)
Design\Prototypes\Daniel\Prototype Image Analyisis\img-anal.py:17:40: E1101: Module 'cv2' has no 'THRESH_BINARY' member (no-member)
Design\Prototypes\Daniel\Prototype Image Analyisis\img-anal.py:18:19: E1101: Module 'cv2' has no 'bitwise_and' member (no-member)
Design\Prototypes\Daniel\Prototype Image Analyisis\img-anal.py:27:20: E1101: Module 'cv2' has no 'resize' member (no-member)
Design\Prototypes\Daniel\Prototype Image Analyisis\img-anal.py:28:65: E1101: Module 'cv2' has no 'INTER_AREA' member (no-member)
Design\Prototypes\Daniel\Prototype Image Analyisis\img-anal.py:35:17: E1101: Module 'cv2' has no 'cvtColor' member (no-member)
Design\Prototypes\Daniel\Prototype Image Analyisis\img-anal.py:35:36: E1101: Module 'cv2' has no 'COLOR_BGR2GRAY' member (no-member)
Design\Prototypes\Daniel\Prototype Image Analyisis\img-anal.py:36:20: E1101: Module 'cv2' has no 'Laplacian' member (no-member)
Design\Prototypes\Daniel\Prototype Image Analyisis\img-anal.py:36:45: E1101: Module 'cv2' has no 'CV_64F' member (no-member)
Design\Prototypes\Daniel\Prototype Image Analyisis\img-anal.py:51:17: E1101: Module 'cv2' has no 'cvtColor' member (no-member)
Design\Prototypes\Daniel\Prototype Image Analyisis\img-anal.py:51:36: E1101: Module 'cv2' has no 'COLOR_BGR2GRAY' member (no-member)
Design\Prototypes\Daniel\Prototype Image Analyisis\img-anal.py:62:16: E1101: Module 'cv2' has no 'cvtColor' member (no-member)
Design\Prototypes\Daniel\Prototype Image Analyisis\img-anal.py:62:35: E1101: Module 'cv2' has no 'COLOR_BGR2HSV' member (no-member)
Design\Prototypes\Daniel\Prototype Image Analyisis\img-anal.py:73:17: E1101: Module 'cv2' has no 'cvtColor' member (no-member)
Design\Prototypes\Daniel\Prototype Image Analyisis\img-anal.py:73:36: E1101: Module 'cv2' has no 'COLOR_BGR2GRAY' member (no-member)
Design\Prototypes\Daniel\Prototype Image Analyisis\img-anal.py:83:16: E1101: Module 'cv2' has no 'cvtColor' member (no-member)
Design\Prototypes\Daniel\Prototype Image Analyisis\img-anal.py:83:35: E1101: Module 'cv2' has no 'COLOR_BGR2HSV' member (no-member)
Design\Prototypes\Daniel\Prototype Image Analyisis\img-anal.py:85:11: E1101: Module 'cv2' has no 'calcHist' member (no-member)
Design\Prototypes\Daniel\Prototype Image Analyisis\img-anal.py:89:21: E1101: Module 'cv2' has no 'cvtColor' member (no-member)
Design\Prototypes\Daniel\Prototype Image Analyisis\img-anal.py:90:54: E1101: Module 'cv2' has no 'COLOR_HSV2BGR' member (no-member)
Design\Prototypes\Daniel\Prototype Image Analyisis\img-anal.py:97:12: E1101: Module 'cv2' has no 'imread' member (no-member)
Design\Prototypes\Daniel\Prototype Image Analyisis\img-anal.py:105:4: E1101: Module 'cv2' has no 'imshow' member (no-member)
Design\Prototypes\Daniel\Prototype Image Analyisis\img-anal.py:106:4: E1101: Module 'cv2' has no 'waitKey' member (no-member)
Design\Prototypes\Daniel\Prototype Image Analyisis\img-anal.py:107:4: E1101: Module 'cv2' has no 'destroyAllWindows' member (no-member)
Design\Prototypes\Daniel\Prototype Image Analyisis\img-anal.py:110:0: C0116: Missing function or method docstring (missing-function-docstring)
Design\Prototypes\Daniel\Prototype Image Analyisis\img-anal.py:119:23: E1101: Module 'cv2' has no 'Mat' member (no-member)
Design\Prototypes\Daniel\Prototype Image Analyisis\img-anal.py:129:12: E1101: Module 'cv2' has no 'imshow' member (no-member)
Design\Prototypes\Daniel\Prototype Image Analyisis\img-anal.py:133:8: E1101: Module 'cv2' has no 'waitKey' member (no-member)
Design\Prototypes\Daniel\Prototype Image Analyisis\img-anal.py:119:8: W0612: Unused variable 'result_image' (unused-variable)
************* Module Design.Prototypes.Daniel.Prototype Image Analyisis.subject_detection
Design\Prototypes\Daniel\Prototype Image Analyisis\subject_detection.py:1:0: C0114: Missing module docstring (missing-module-docstring)
Design\Prototypes\Daniel\Prototype Image Analyisis\subject_detection.py:8:12: E1101: Module 'cv2' has no 'imread' member (no-member)
Design\Prototypes\Daniel\Prototype Image Analyisis\subject_detection.py:19:11: E1101: Module 'cv2' has no 'cvtColor' member (no-member)
Design\Prototypes\Daniel\Prototype Image Analyisis\subject_detection.py:19:30: E1101: Module 'cv2' has no 'COLOR_BGR2GRAY' member (no-member)
Design\Prototypes\Daniel\Prototype Image Analyisis\subject_detection.py:20:16: E1101: Module 'cv2' has no 'Laplacian' member (no-member)
Design\Prototypes\Daniel\Prototype Image Analyisis\subject_detection.py:20:35: E1101: Module 'cv2' has no 'CV_64F' member (no-member)
Design\Prototypes\Daniel\Prototype Image Analyisis\subject_detection.py:22:21: E1101: Module 'cv2' has no 'normalize' member (no-member)
Design\Prototypes\Daniel\Prototype Image Analyisis\subject_detection.py:22:61: E1101: Module 'cv2' has no 'NORM_MINMAX' member (no-member)
Design\Prototypes\Daniel\Prototype Image Analyisis\subject_detection.py:24:11: E1101: Module 'cv2' has no 'GaussianBlur' member (no-member)
Design\Prototypes\Daniel\Prototype Image Analyisis\subject_detection.py:25:11: E1101: Module 'cv2' has no 'threshold' member (no-member)
Design\Prototypes\Daniel\Prototype Image Analyisis\subject_detection.py:25:40: E1101: Module 'cv2' has no 'THRESH_BINARY' member (no-member)
Design\Prototypes\Daniel\Prototype Image Analyisis\subject_detection.py:26:19: E1101: Module 'cv2' has no 'bitwise_and' member (no-member)
Design\Prototypes\Daniel\Prototype Image Analyisis\subject_detection.py:35:20: E1101: Module 'cv2' has no 'resize' member (no-member)
Design\Prototypes\Daniel\Prototype Image Analyisis\subject_detection.py:36:65: E1101: Module 'cv2' has no 'INTER_AREA' member (no-member)
Design\Prototypes\Daniel\Prototype Image Analyisis\subject_detection.py:41:0: C0116: Missing function or method docstring (missing-function-docstring)
Design\Prototypes\Daniel\Prototype Image Analyisis\subject_detection.py:48:4: W0621: Redefining name 'grid_of_images' from outer scope (line 41) (redefined-outer-name)
Design\Prototypes\Daniel\Prototype Image Analyisis\subject_detection.py:60:22: E1101: Module 'cv2' has no 'resize' member (no-member)
Design\Prototypes\Daniel\Prototype Image Analyisis\subject_detection.py:61:58: E1101: Module 'cv2' has no 'INTER_AREA' member (no-member)
Design\Prototypes\Daniel\Prototype Image Analyisis\subject_detection.py:41:43: W0613: Unused argument 'max_height' (unused-argument)
Design\Prototypes\Daniel\Prototype Image Analyisis\subject_detection.py:70:0: C0116: Missing function or method docstring (missing-function-docstring)
Design\Prototypes\Daniel\Prototype Image Analyisis\subject_detection.py:92:12: E1101: Module 'cv2' has no 'putText' member (no-member)
Design\Prototypes\Daniel\Prototype Image Analyisis\subject_detection.py:96:16: E1101: Module 'cv2' has no 'FONT_HERSHEY_SIMPLEX' member (no-member)
Design\Prototypes\Daniel\Prototype Image Analyisis\subject_detection.py:105:8: E1101: Module 'cv2' has no 'imwrite' member (no-member)
Design\Prototypes\Daniel\Prototype Image Analyisis\subject_detection.py:107:8: E1101: Module 'cv2' has no 'imshow' member (no-member)
Design\Prototypes\Daniel\Prototype Image Analyisis\subject_detection.py:108:8: E1101: Module 'cv2' has no 'waitKey' member (no-member)
Design\Prototypes\Daniel\Prototype Image Analyisis\subject_detection.py:3:0: C0411: standard import "sys" should be placed before third party imports "cv2", "numpy" (wrong-import-order)
************* Module Design.Prototypes.Daniel.PrototypeGUI.gui-test
Design\Prototypes\Daniel\PrototypeGUI\gui-test.py:1:0: C0114: Missing module docstring (missing-module-docstring)
Design\Prototypes\Daniel\PrototypeGUI\gui-test.py:1:0: C0103: Module name "gui-test" doesn't conform to snake_case naming style (invalid-name)
Design\Prototypes\Daniel\PrototypeGUI\gui-test.py:1:0: E0401: Unable to import 'PyQt5' (import-error)
Design\Prototypes\Daniel\PrototypeGUI\gui-test.py:6:0: C0116: Missing function or method docstring (missing-function-docstring)
Design\Prototypes\Daniel\PrototypeGUI\gui-test.py:7:4: W0621: Redefining name 'card' from outer scope (line 73) (redefined-outer-name)
************* Module tests.test_unittest
tests\test_unittest.py:1:0: C0114: Missing module docstring (missing-module-docstring)
tests\test_unittest.py:4:0: C0115: Missing class docstring (missing-class-docstring)
tests\test_unittest.py:4:0: C0103: Class name "unittest_test" doesn't conform to PascalCase naming style (invalid-name)
tests\test_unittest.py:5:4: C0116: Missing function or method docstring (missing-function-docstring)
tests\test_unittest.py:1:0: R0801: Similar lines in 2 files
==photo_viewer:[68:102]
==single_photo_viewer:[58:93]
        self.feedback_box.configure(
            bg="#1e1e1e",
            fg="#ffffff",
            insertbackground="#ffffff",
            relief="flat",
            padx=10,
            pady=10,
        )
        self.feedback_box.grid(row=0, column=0, sticky="nsew", padx=(0, 8), pady=(0, 8))

        self.gen_btn = ttk.Button(
            self.feedback_card,
            text="Generate feedback",
            bootstyle="primary",
            command=self.generate_feedback_for_current,
        )
        self.gen_btn.grid(row=1, column=0, sticky="w", pady=(4, 0))

        self.feedback_card.columnconfigure(0, weight=1)
        self.feedback_card.rowconfigure(0, weight=1)

        self.feedback_card.place(
            relx=0.0, rely=1.0, x=12, y=-12, anchor="sw", width=360
        )
        self.feedback_card.lift()
        # ------------------------------------------------------------

        def _set_feedback(text: str):
            self.feedback_box.configure(state="normal")
            self.feedback_box.delete("1.0", "end")
            self.feedback_box.insert("1.0", text)
            self.feedback_box.configure(state="disabled")

        self._set_feedback = _set_feedback
 (duplicate-code)
tests\test_unittest.py:1:0: R0801: Similar lines in 2 files
==Design.Prototypes.Daniel.Prototype Image Analyisis.img-anal:[10:34]
==Design.Prototypes.Daniel.Prototype Image Analyisis.subject_detection:[18:41]
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    laplacian = cv.Laplacian(gray, cv.CV_64F)
    sharpness_map = np.abs(laplacian)
    norm_sharpness = cv.normalize(sharpness_map, None, 0, 1, cv.NORM_MINMAX)
    mask = (norm_sharpness > focus_threshold).astype(np.uint8) * 255
    mask = cv.GaussianBlur(mask, (11, 11), 0)
    mask = cv.threshold(mask, 127, 255, cv.THRESH_BINARY)[1]
    masked_image = cv.bitwise_and(image, image, mask=mask)
    return masked_image


def rezize_image_preserve_aspect_ratio(image, target_width=960):
    """Resize an image while preserving its aspect ratio."""
    height, width = image.shape[:2]
    aspect_ratio = width / height
    target_height = int(target_width / aspect_ratio)
    resized_image = cv.resize(
        image, (int(target_width), target_height), interpolation=cv.INTER_AREA
    )
    return resized_image


def detect_sharpness(image):
    """Detect the sharpness of an image as a proportion between 0 (blurry) and 1 (sharp).""" (duplicate-code)
tests\test_unittest.py:1:0: R0801: Similar lines in 2 files
==base_viewer:[26:38]
==photo_scorer:[26:38]
        raw_extensions = {
            ".cr2",
            ".nef",
            ".arw",
            ".dng",
            ".rw2",
            ".orf",
            ".raf",
            ".srw",
            ".pef",
        }
        ext = os.path.splitext(file_path)[1].lower() (duplicate-code)
tests\test_unittest.py:1:0: R0801: Similar lines in 2 files
==photo_viewer:[346:357]
==single_photo_viewer:[171:184]
            try:
                exif = self.db.get_exif(pid)
            except Exception:
                exif = None

            try:
                if hasattr(self.db, "get_scores") and callable(self.db.get_scores):
                    scores = self.db.get_scores(pid)
                else:
                    scores = {"quality": self.db.get_quality_score(pid)}
            except Exception:
                scores = None
 (duplicate-code)
tests\test_unittest.py:1:0: R0801: Similar lines in 2 files
==base_viewer:[26:37]
==exif_reader:[19:30]
        raw_extensions = {
            ".cr2",
            ".nef",
            ".arw",
            ".dng",
            ".rw2",
            ".orf",
            ".raf",
            ".srw",
            ".pef",
        } (duplicate-code)
tests\test_unittest.py:1:0: R0801: Similar lines in 2 files
==base_viewer:[27:36]
==photo_importer:[15:24]
        ".cr2",
        ".nef",
        ".arw",
        ".dng",
        ".rw2",
        ".orf",
        ".raf",
        ".srw",
        ".pef", (duplicate-code)

------------------------------------------------------------------
Your code has been rated at 6.63/10 (previous run: 6.61/10, +0.02)