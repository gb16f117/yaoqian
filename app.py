from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import sqlite3
import random
import os

app = Flask(__name__)
CORS(app)

# 六十甲子签数据（完整版）
FORTUNE_DATA = [
    {"sequence": 1, "name": "甲子签", "level": "上上", "content": "天开子位万象新，\n木火通明福运临，\n贵人相助前程远，\n如意吉祥事事顺。", "interpretation": "此签为大吉之兆，万物复苏之时，一切重新开始。事业上会有贵人相助，前程远大。财运亨通，家庭和睦。所求之事皆能顺遂，是难得的上上签。适合创业、投资、婚嫁等重大决定。"},
    {"sequence": 2, "name": "乙丑签", "level": "上中", "content": "金锁两重关难越，\n诚实守信解忧愁，\n坚心忍耐终有日，\n云开月照见高楼。", "interpretation": "此签预示当前可能面临一些困难，如同金锁双重关。但只要保持诚信，坚定心志，终会柳暗花明。需要耐心等待时机，不要急于求成。感情方面需多沟通，事业方面稳扎稳打。"},
    {"sequence": 3, "name": "丙寅签", "level": "上上", "content": "清新绿芋生机现，\n阳气初升势如竹，\n奋发图强成大业，\n功名利禄自然来。", "interpretation": "此签为吉兆，如同春天的绿芋，充满生机。阳气上升，势如破竹。是行动的最佳时机，事业上要积极进取，会有不错的成绩。财运方面有贵人相助，家庭幸福美满。"},
    {"sequence": 4, "name": "丁卯签", "level": "中上", "content": "朱纸上好语留香，\n文字传播福运长，\n文采飞扬名声起，\n学问精深前程广。", "interpretation": "此签与文字、学问相关，适合从事写作、出版、教育等行业。名声会逐渐传开，获得他人的认可。考试、求职会有好成绩。感情方面通过沟通能增进了解。"},
    {"sequence": 5, "name": "戊辰签", "level": "上上", "content": "峰回路转奇人现，\n土厚水深福泽绵，\n前途光明运道好，\n多行善事保平安。", "interpretation": "此签为大吉，如同峰回路转，前途光明。土厚水深，寓意根基稳固，福泽深厚。财运亨通，事业发展顺利。要多做善事积德，保持谦逊态度，会有贵人相助。"},
    {"sequence": 6, "name": "己巳签", "level": "中上", "content": "春来秋去无穷意，\n田园藏火照归途，\n进退有度谋略深，\n福慧双修得安舒。", "interpretation": "此签提示要懂得进退，有谋有略。如同田园藏火，外柔内刚。工作上要善于规划，感情上要适度沟通。财运方面稳中求进，不可贪心。身体健康方面要注意保养。"},
    {"sequence": 7, "name": "庚午签", "level": "上中", "content": "金映骄阳光芒盛，\n刚毅重诺声名扬，\n锋芒毕露成大事，\n功名可期在前方。", "interpretation": "此签为吉兆，金映骄阳，光芒四射。为人刚毅，重信守诺，会赢得他人的尊重和信任。事业上能取得成就，名声远扬。但要避免锋芒过露，注意低调行事。"},
    {"sequence": 8, "name": "辛未签", "level": "中上", "content": "珠玉藏土外冷内，\n精于筹谋晚运昌，\n外表温和心如铁，\n待时而动创辉煌。", "interpretation": "此签提醒要善于谋略，外表温和，内心坚毅。时机未到时要多等待，不可轻举妄动。晚运较好，年轻时多积累经验和人脉。财运方面要善于理财，感情上要有耐心。"},
    {"sequence": 9, "name": "壬申签", "level": "上上", "content": "江河过峡智勇全，\n变动之中求发展，\n四海通达皆朋友，\n乘风破浪济沧海。", "interpretation": "此签为大吉，智勇双全，能在变动中寻找机会。人脉广阔，四海皆有朋友。适合外出发展，或从事与水、交通、贸易相关的行业。事业上会有大发展，财运亨通。"},
    {"sequence": 10, "name": "癸酉签", "level": "中上", "content": "雨露淬金聪慧显，\n外圆内方情义全，\n细致观察人缘好，\n福慧双修保平安。", "interpretation": "此签为人聪慧，善于观察，外圆内方，处世圆滑但不失原则。人缘极佳，朋友众多。财运方面有小财运，感情上要注意沟通。健康方面要注意休息。"},
    {"sequence": 11, "name": "甲戌签", "level": "上中", "content": "栋梁固城根基稳，\n正直不阿持家道，\n门庭兴旺子孙贤，\n福寿绵长乐逍遥。", "interpretation": "此签为吉兆，如同栋梁之材，根基稳固。为人正直，持家有方，家庭兴旺，子孙贤孝。事业上有贵人相助，财运平稳。健康方面注意保养，长寿之兆。"},
    {"sequence": 12, "name": "乙亥签", "level": "中上", "content": "柳丝拂波柔韧显，\n福慧双修顺且安，\n善于交际人缘好，\n贵人在前福泽长。", "interpretation": "此签为吉兆，性格柔和，善于交际，人缘极佳。有贵人相助，事业发展顺利。财运方面稳步前进，感情上要专一。健康方面要注意饮食和作息。"},
    {"sequence": 13, "name": "丙子签", "level": "中下", "content": "湖心焰影外动静，\n才情卓绝起伏真，\n波澜不惊心如水，\n待时而动事可成。", "interpretation": "此签为中下签，提醒要保持内心的平静，外动内静。才情出众，但要注意把握机会。事业上起伏不定，需要耐心等待。财运方面不宜投机，感情上要多理解。"},
    {"sequence": 14, "name": "丁丑签", "level": "中中", "content": "炉火炼金精雕琢，\n大器晚成志不移，\n外显内敛藏锋芒，\n待到时机耀光芒。", "interpretation": "此签为大器晚成之兆，如同炉火炼金，需要经过考验。年轻时要多积累，不要急于求成。事业上晚运较好，财运方面要稳扎稳打。感情上要有耐心。"},
    {"sequence": 15, "name": "戊寅签", "level": "上上", "content": "高山立木胸怀广，\n敢为人先名利双，\n开创进取成大业，\n福泽深厚子孙昌。", "interpretation": "此签为大吉，胸怀宽广，敢于开创，会名利双收。事业上要积极主动，会有不错的发展。财运亨通，家庭幸福。但要避免过于冒险，要稳步前进。"},
    {"sequence": 16, "name": "己卯签", "level": "上中", "content": "沃土培花温润显，\n善理财务家业兴，\n细致入微人缘好，\n福星高照事事顺。", "interpretation": "此签为吉兆，如同沃土培花，温润细腻。善于理财，家业兴旺。为人细致，人缘极佳。事业上有贵人相助，财运平稳。感情上要用心经营。"},
    {"sequence": 17, "name": "庚辰签", "level": "上上", "content": "剑藏深潭刚柔济，\n伺机而动终成业，\n时来运转福运至，\n智勇双全天下知。", "interpretation": "此签为大吉，如同宝剑藏于深潭，刚柔并济。要善于等待时机，伺机而动。时来运转时，事业会有大发展，名声远扬。财运亨通，但要注意把握时机。"},
    {"sequence": 18, "name": "辛巳签", "level": "上中", "content": "精金熔火革新意，\n智破困局显奇才，\n功成身退留名在，\n福泽绵长子孙贤。", "interpretation": "此签为吉兆，善于革新，能够解决困难。事业上会有成就，但要知道适可而止。财运方面有进有出，要注意理财。感情上要专一，健康方面注意休息。"},
    {"sequence": 19, "name": "壬午签", "level": "上上", "content": "江海蒸霞智勇全，\n奔波见利名四方，\n贵人相助前程远，\n福星高照万事安。", "interpretation": "此签为大吉，智勇双全，奔波之中会有收获。名扬四方，前程远大。有贵人相助，事业发展顺利。财运亨通，家庭幸福。适合外出发展。"},
    {"sequence": 20, "name": "癸未签", "level": "中上", "content": "甘露润土外谦明，\n贵人提携福寿增，\n低调做人高调事，\n待时而动万事成。", "interpretation": "此签为吉兆，为人低调谦逊，会有贵人提携。要低调做人，高调做事，会有不错的成就。财运方面稳步前进，感情上要有耐心。健康方面注意保养。"},
    {"sequence": 21, "name": "甲申签", "level": "上上", "content": "青松立崖自坚强，\n逆流而上终成祥，\n独立进取创大业，\n福泽深厚万年长。", "interpretation": "此签为大吉，如同青松立于悬崖，独立自强。在逆境中坚持进取，最终会成功。事业上要积极主动，会有大发展。财运亨通，家庭幸福。"},
    {"sequence": 22, "name": "乙酉签", "level": "中上", "content": "泉中水清智慧显，\n乐观通达人缘佳，\n口快心直易得友，\n福星高照事事华。", "interpretation": "此签为吉兆，为人乐观，口快心直，容易交到朋友。智慧出众，人缘极佳。事业上有贵人相助，财运平稳。感情上要真诚，健康方面要注意。"},
    {"sequence": 23, "name": "丙戌签", "level": "中中", "content": "山头火热情坦荡，\n口快舌伶身闲心，\n少年奔波中年旺，\n晚景福禄寿延年。", "interpretation": "此签为性格坦荡，口快心直。少年时奔波劳碌，中年时运势转旺，晚年福禄双全。事业上要努力，财运方面稳中求进。感情上要多沟通。"},
    {"sequence": 24, "name": "丁亥签", "level": "下", "content": "屋上火光照四邻，\n外柔内刚志气深，\n待人接物须诚善，\n福星高照保安宁。", "interpretation": "此签为下签，提醒要待人真诚，外柔内刚。志气深远，但要注意方式方法。事业上要脚踏实地，财运方面不宜投机。感情上要专一，健康方面注意保养。"},
    {"sequence": 25, "name": "戊子签", "level": "上上", "content": "霹雳火光明四照，\n雷声震动万方知，\n声名远扬前程广，\n福泽深厚乐逍遥。", "interpretation": "此签为大吉，声名远扬，前程广阔。如同霹雳火，光芒四照。事业上会有大发展，名声远播。财运亨通，家庭幸福。但要避免过于张扬。"},
    {"sequence": 26, "name": "己丑签", "level": "中上", "content": "霹雳火雷震四野，\n威严显赫名自扬，\n稳步前进成大业，\n福星高照保安康。", "interpretation": "此签为吉兆，威严显赫，名扬四海。事业上要稳步前进，会有不错的成就。财运方面稳中求进，感情上要真诚。健康方面注意保养。"},
    {"sequence": 27, "name": "庚寅签", "level": "上中", "content": "松柏木坚韧刚强，\n经冬不凋志气昂，\n历经风雨终成材，\n福泽深厚万年长。", "interpretation": "此签为吉兆，如同松柏，坚韧刚强。经历风雨之后，终会成材。事业上要坚持不懈，会有不错的成就。财运方面稳扎稳打，感情上要有耐心。"},
    {"sequence": 28, "name": "辛卯签", "level": "中上", "content": "松柏木立寒风中，\n傲骨铮铮志气雄，\n坚持到底终有日，\n功成名就乐无穷。", "interpretation": "此签为吉兆，如同寒风中的松柏，傲骨铮铮。要坚持到底，终会成功。事业上要有恒心，财运方面稳中求进。感情上要专一，健康方面注意。"},
    {"sequence": 29, "name": "壬辰签", "level": "上上", "content": "长流水波涛滚滚，\n源远流长福泽深，\n乘风破浪济沧海，\n功成名就耀门庭。", "interpretation": "此签为大吉，如同长流水，源远流长。乘风破浪，会有大发展。事业有成，名扬四方。财运亨通，家庭幸福。适合外出发展。"},
    {"sequence": 30, "name": "癸巳签", "level": "中上", "content": "长流水清见底透，\n心地纯净人缘佳，\n顺势而为事可成，\n福星高照乐年华。", "interpretation": "此签为吉兆，心地纯净，人缘极佳。要顺势而为，会有不错的成就。事业上要灵活，财运方面稳扎稳打。感情上要真诚，健康方面注意。"},
    {"sequence": 31, "name": "甲午签", "level": "中中", "content": "沙中金藏深土内，\n待时而动显锋芒，\n韬光养晦时机到，\n一举成名天下知。", "interpretation": "此签为韬光养晦之兆，如同沙中金，藏于土内。要等待时机，不可急于求成。时机成熟时，一举成名。事业上要耐心，财运方面要善于理财。"},
    {"sequence": 32, "name": "乙未签", "level": "中上", "content": "沙中金光内敛藏，\n外冷内热心志强，\n精明能干成大事，\n福泽深厚万年长。", "interpretation": "此签为吉兆，外冷内热，志向远大。精明能干，会成大事。事业上要积极主动，财运方面稳扎稳打。感情上要专一，健康方面注意。"},
    {"sequence": 33, "name": "丙申签", "level": "上中", "content": "山下火光明温暖，\n照耀四方福泽长，\n待人真诚人缘好，\n事业有成乐安康。", "interpretation": "此签为吉兆，光明温暖，福泽深厚。待人真诚，人缘极佳。事业上会有不错的成就，财运方面稳中求进。感情上要用心经营，健康方面注意。"},
    {"sequence": 34, "name": "丁酉签", "level": "中上", "content": "山下火照耀四野，\n温暖人心福自至，\n诚恳待人朋友多，\n事业兴旺财气聚。", "interpretation": "此签为吉兆，温暖人心，福气自来。诚恳待人，朋友众多。事业兴旺，财运亨通。感情上要真诚，健康方面注意保养。"},
    {"sequence": 35, "name": "戊戌签", "level": "下下", "content": "大林木生机旺盛，\n根深叶茂福泽长，\n稳步前进成大业，\n子孙贤孝乐安康。", "interpretation": "此签为下下签，为生机旺盛，根深叶茂。要稳步前进，会有不错的成就。事业上要坚持，财运方面稳中求进。家庭和睦，子孙贤孝。"},
    {"sequence": 36, "name": "己亥签", "level": "中中", "content": "大林木立平原上，\n枝繁叶茂福泽长，\n脚踏实地成大业，\n福星高照乐安康。", "interpretation": "此签为脚踏实地，稳步前进。如同大树，枝繁叶茂。事业上要坚持不懈，财运方面稳扎稳打。感情上要专一，健康方面注意。"},
    {"sequence": 37, "name": "庚子签", "level": "上上", "content": "壁上土坚固如石，\n根基深厚福泽长，\n稳扎稳打成大业，\n子孙贤孝乐安康。", "interpretation": "此签为大吉，根基深厚，坚固如石。要稳扎稳打，会有大发展。事业上要有恒心，财运方面稳步前进。家庭和睦，子孙贤孝。"},
    {"sequence": 38, "name": "辛丑签", "level": "中上", "content": "壁上土坚固耐用，\n根基稳固福泽长，\n精心耕耘成大业，\n福星高照乐安康。", "interpretation": "此签为吉兆，根基稳固，福泽深厚。要精心耕耘，会有不错的成就。事业上要有耐心，财运方面稳扎稳打。感情上要专一，健康方面注意。"},
    {"sequence": 39, "name": "壬寅签", "level": "上中", "content": "金箔金珍贵华美，\n外华内实福泽长，\n待价而沽时机到，\n一举成名天下知。", "interpretation": "此签为吉兆，外华内实，珍贵华美。要待价而沽，等待时机。时机成熟时，一举成名。事业上要耐心，财运方面要善于理财。"},
    {"sequence": 40, "name": "癸卯签", "level": "中中", "content": "金箔金光闪闪亮，\n内藏锋芒志气昂，\n韬光养晦待时机，\n功成名就乐逍遥。", "interpretation": "此签为韬光养晦，内藏锋芒。要等待时机，不可急于求成。时机成熟时，功成名就。事业上要有耐心，财运方面要善于理财。"},
    {"sequence": 41, "name": "甲辰签", "level": "上上", "content": "覆灯火光明四照，\n照耀前程福泽长，\n声名远扬成大业，\n子孙贤孝乐安康。", "interpretation": "此签为大吉，光明四照，福泽深厚。声名远扬，前程广阔。事业上会有大发展，财运亨通。家庭和睦，子孙贤孝。"},
    {"sequence": 42, "name": "乙巳签", "level": "中上", "content": "覆灯火温暖人心，\n照亮前程福泽长，\n诚恳待人朋友多，\n事业兴旺财气聚。", "interpretation": "此签为吉兆，温暖人心，福气自来。诚恳待人，朋友众多。事业兴旺，财运亨通。感情上要真诚，健康方面注意保养。"},
    {"sequence": 43, "name": "丙午签", "level": "上上", "content": "天河水浩浩荡荡，\n源远流长福泽深，\n乘风破浪济沧海，\n功成名就耀门庭。", "interpretation": "此签为大吉，如同天河水，浩浩荡荡。乘风破浪，会有大发展。事业有成，名扬四方。财运亨通，家庭幸福。适合外出发展。"},
    {"sequence": 44, "name": "丁未签", "level": "上中", "content": "天河水清见底透，\n心地纯净人缘佳，\n顺势而为事可成，\n福星高照乐年华。", "interpretation": "此签为吉兆，心地纯净，人缘极佳。要顺势而为，会有不错的成就。事业上要灵活，财运方面稳扎稳打。感情上要真诚，健康方面注意。"},
    {"sequence": 45, "name": "戊申签", "level": "中中", "content": "大驿土厚德载物，\n包容四方福泽长，\n稳扎稳打成大业，\n福星高照乐安康。", "interpretation": "此签为厚德载物，包容四方。要稳扎稳打，会有不错的成就。事业上要坚持，财运方面稳中求进。家庭和睦，子孙贤孝。健康方面注意。"},
    {"sequence": 46, "name": "己酉签", "level": "中中", "content": "大驿土承载万物，\n根基稳固福泽长，\n脚踏实地成大业，\n子孙贤孝乐安康。", "interpretation": "此签为脚踏实地，稳步前进。根基稳固，福泽深厚。事业上要坚持不懈，财运方面稳扎稳打。感情上要专一，健康方面注意。"},
    {"sequence": 47, "name": "庚戌签", "level": "上上", "content": "钗钏金珍贵华美，\n外华内实福泽长，\n精心雕琢成大器，\n功成名就乐逍遥。", "interpretation": "此签为大吉，珍贵华美，外华内实。精心雕琢，终成大器。事业上要用心，财运方面稳步前进。家庭幸福，子孙贤孝。"},
    {"sequence": 48, "name": "辛亥签", "level": "中上", "content": "钗钏金光闪闪亮，\n内藏锋芒志气昂，\n待价而沽时机到，\n一举成名天下知。", "interpretation": "此签为吉兆，内藏锋芒，志向远大。要待价而沽，等待时机。时机成熟时，一举成名。事业上要耐心，财运方面要善于理财。"},
    {"sequence": 49, "name": "壬子签", "level": "上上", "content": "桑柘木生机盎然，\n根深叶茂福泽长，\n精心培育成大业，\n子孙贤孝乐安康。", "interpretation": "此签为大吉，生机盎然，根深叶茂。精心培育，会有大发展。事业上要用心，财运方面稳步前进。家庭和睦，子孙贤孝。"},
    {"sequence": 50, "name": "癸丑签", "level": "中上", "content": "桑柘木立平原上，\n枝繁叶茂福泽长，\n稳步前进成大业，\n福星高照乐安康。", "interpretation": "此签为吉兆，枝繁叶茂，福泽深厚。要稳步前进，会有不错的成就。事业上要坚持，财运方面稳中求进。感情上要专一，健康方面注意。"},
    {"sequence": 51, "name": "甲寅签", "level": "上上", "content": "大溪水波涛汹涌，\n奔腾不息福泽深，\n乘风破浪济沧海，\n功成名就耀门庭。", "interpretation": "此签为大吉，波涛汹涌，奔腾不息。乘风破浪，会有大发展。事业有成，名扬四方。财运亨通，家庭幸福。适合外出发展。"},
    {"sequence": 52, "name": "乙卯签", "level": "上中", "content": "大溪水清流不断，\n源远流长福泽深，\n顺势而为事可成，\n福星高照乐年华。", "interpretation": "此签为吉兆，源远流长，福泽深厚。要顺势而为，会有不错的成就。事业上要灵活，财运方面稳扎稳打。感情上要真诚，健康方面注意。"},
    {"sequence": 53, "name": "丙辰签", "level": "中中", "content": "沙中土细腻温润，\n滋养万物福泽长，\n精心耕耘成大业，\n福星高照乐安康。", "interpretation": "此签为细腻温润，滋养万物。要精心耕耘，会有不错的成就。事业上要有耐心，财运方面稳扎稳打。家庭和睦，子孙贤孝。健康方面注意。"},
    {"sequence": 54, "name": "丁巳签", "level": "中中", "content": "沙中土承载万物，\n根基稳固福泽长，\n脚踏实地成大业，\n子孙贤孝乐安康。", "interpretation": "此签为脚踏实地，稳步前进。根基稳固，福泽深厚。事业上要坚持不懈，财运方面稳扎稳打。感情上要专一，健康方面注意。"},
    {"sequence": 55, "name": "戊午签", "level": "上上", "content": "天上火光明普照，\n照耀四方福泽长，\n声名远扬成大业，\n子孙贤孝乐安康。", "interpretation": "此签为大吉，光明普照，福泽深厚。声名远扬，前程广阔。事业上会有大发展，财运亨通。家庭和睦，子孙贤孝。"},
    {"sequence": 56, "name": "己未签", "level": "上中", "content": "天上火温暖四野，\n照亮前程福泽长，\n诚恳待人朋友多，\n事业兴旺财气聚。", "interpretation": "此签为吉兆，温暖四野，福气自来。诚恳待人，朋友众多。事业兴旺，财运亨通。感情上要真诚，健康方面注意保养。"},
    {"sequence": 57, "name": "庚申签", "level": "上上", "content": "石榴木果实累累，\n福泽深厚子孙昌，\n精心培育成大业，\n功成名就乐逍遥。", "interpretation": "此签为大吉，果实累累，子孙昌盛。精心培育，会有大发展。事业上要用心，财运方面稳步前进。家庭幸福，子孙贤孝。"},
    {"sequence": 58, "name": "辛酉签", "level": "中上", "content": "石榴木花开富贵，\n根深叶茂福泽长，\n稳步前进成大业，\n福星高照乐安康。", "interpretation": "此签为吉兆，花开富贵，福泽深厚。要稳步前进，会有不错的成就。事业上要坚持，财运方面稳中求进。感情上要专一，健康方面注意。"},
    {"sequence": 59, "name": "壬戌签", "level": "中中", "content": "大海水波澜壮阔，\n包容万物福泽长，\n乘风破浪济沧海，\n功成名就耀门庭。", "interpretation": "此签为波澜壮阔，包容万物。要乘风破浪，会有不错的成就。事业上要有勇气，财运方面稳中求进。家庭和睦，子孙贤孝。适合外出发展。"},
    {"sequence": 60, "name": "癸亥签", "level": "中中", "content": "大海水浩瀚无边，\n源远流长福泽深，\n顺势而为事可成，\n福星高照乐年华。", "interpretation": "此签为浩瀚无边，源远流长。要顺势而为，会有不错的成就。事业上要灵活，财运方面稳扎稳打。感情上要真诚，健康方面注意。"}
]

# 数据库初始化
def init_db():
    conn = sqlite3.connect('fortune.db')
    c = conn.cursor()
    
    # 创建签文表
    c.execute('''
        CREATE TABLE IF NOT EXISTS fortunes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sequence INTEGER NOT NULL UNIQUE,
            name TEXT NOT NULL UNIQUE,
            level TEXT NOT NULL,
            content TEXT NOT NULL,
            interpretation TEXT NOT NULL
        )
    ''')
    
    # 插入签文数据
    c.execute('SELECT COUNT(*) FROM fortunes')
    count = c.fetchone()[0]
    
    if count == 0:
        for fortune in FORTUNE_DATA:
            c.execute('''
                INSERT INTO fortunes (sequence, name, level, content, interpretation)
                VALUES (?, ?, ?, ?, ?)
            ''', (fortune['sequence'], fortune['name'], fortune['level'], fortune['content'], fortune['interpretation']))
        conn.commit()
        print(f"已插入 {len(FORTUNE_DATA)} 条签文数据")
    
    conn.close()

# 数据库连接
def get_db_connection():
    conn = sqlite3.connect('fortune.db')
    conn.row_factory = sqlite3.Row
    return conn

# API路由
@app.route('/')
def index():
    """首页"""
    return send_from_directory('frontend', 'index.html')

@app.route('/<path:filename>')
def static_files(filename):
    """静态文件"""
    return send_from_directory('frontend', filename)

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'ok', 'message': 'Server is running'})

@app.route('/api/draw', methods=['POST'])
def draw_fortune():
    """随机抽取一支签"""
    conn = get_db_connection()
    
    # 随机抽取一支签
    c = conn.cursor()
    c.execute('SELECT * FROM fortunes ORDER BY RANDOM() LIMIT 1')
    fortune = c.fetchone()
    conn.close()
    
    if fortune:
        return jsonify({
            'id': fortune['id'],
            'sequence': fortune['sequence'],
            'name': fortune['name'],
            'level': fortune['level'],
            'content': fortune['content'],
            'interpretation': fortune['interpretation']
        })
    
    return jsonify({'error': 'No fortune found'}), 404

@app.route('/api/fortunes/<int:fortune_id>', methods=['GET'])
def get_fortune(fortune_id):
    """获取指定签文的详细信息"""
    conn = get_db_connection()
    fortune = conn.execute('SELECT * FROM fortunes WHERE id = ?', (fortune_id,)).fetchone()
    conn.close()
    
    if fortune:
        return jsonify({
            'id': fortune['id'],
            'sequence': fortune['sequence'],
            'name': fortune['name'],
            'level': fortune['level'],
            'content': fortune['content'],
            'interpretation': fortune['interpretation']
        })
    
    return jsonify({'error': 'Fortune not found'}), 404

@app.route('/api/fortunes', methods=['GET'])
def list_fortunes():
    """获取所有签文列表"""
    conn = get_db_connection()
    fortunes = conn.execute('SELECT id, sequence, name, level FROM fortunes ORDER BY sequence').fetchall()
    conn.close()
    
    return jsonify([dict(fortune) for fortune in fortunes])

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5004)
