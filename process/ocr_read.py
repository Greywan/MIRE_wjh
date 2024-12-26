from paddleocr import PaddleOCR

class OcrImageToText:
    def init_model(self, lang="ch"):
        self.ocr = PaddleOCR(use_angle_cls=True, lang=lang)

    def ocr_image_to_string(self, image_path):
        # 初始化PaddleOCR，设置语言为中文，并启用方向分类器
        
        # 对图片进行OCR识别
        result = self.ocr.ocr(image_path, cls=True)
        words = []
        if not result or not result[0]:
            return ''
        for line in result[0]:
            text = line[1][0]
            confidence = line[1][1]
            box = line[0]
            words.append(text)
        # # 提取所有识别到的文本信息
        # words = [line[1][0] for line in result]
        
        # 将所有文本信息用逗号相连
        output_string = ','.join(words)
        
        return output_string

# # 示例图片路径
# image_path = 'path_to_your_image.jpg'

# # 调用函数并输出结果
# output_string = ocr_image_to_string(image_path)
# print(output_string)