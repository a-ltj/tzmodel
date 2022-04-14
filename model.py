

import pandas as pd
import base64
import os

from services.image_parser import parse_image

LABEL_NAME = 'class'


class PyModel(object):

    def __init__(self):
        pass

    def load(self):
        pass

    def transform(self, dataset):  # type:(pd.DataFrame)->pd.DataFrame
        """
        :param dataset: {"data": {"type": 场站中文名_场站类型, "image": 图片的base64编码}}
        :return: {"0": {"prediction": XML格式的结果}}
        """
        image_type = dataset['data']['type']
        image_path = dataset['data']['image']
        # img = base64.b64decode(image)
        #
        # rtfile = open('test/tmp/43_transformer.jpg', 'wb+')
        # rtfile.write(img)
        # rtfile.close()
        # image_path = 'test/tmp/43_transformer.jpg'
        # print(image_path )

        res_xml = parse_image(image_type, image_path)


        return pd.DataFrame({'prediction': res_xml}, index=[0])
if __name__ =='__main__':
    pymodel = PyModel()
    img_path = 'test/tmp/43_transformer.jpg'
    # with open(img_path, 'rb') as f:
    #     image_data = f.read()
        #base64_data = base64.b64encode(image_data)  # base64编码
        #base64_str = str(base64_data, 'utf-8')
    data = {"data": {"type": '43_transformer', "image": img_path}}
    image_type = data['data']['type']

    result_xml = pymodel.transform(data)
    xml = result_xml['prediction'][0]
    folder = 'result/'
    if not os.path.exists(folder):
        os.makedirs(folder)
    xml_name = folder + image_type +'.xml'
    print(xml_name)
    f = open(xml_name, 'w', encoding='utf-8')
    f.write(xml)
    f.close

