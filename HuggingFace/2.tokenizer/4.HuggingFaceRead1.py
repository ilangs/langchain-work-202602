#3.huggingfaceread.py

from datasets import load_dataset

#1.허깅페이스 허브에서 rotten_tomatoes (영화리뷰)
dataset = load_dataset("rotten_tomatoes")

#2.데이터셋의 구조(train,validation,test)를 확인
print('데이터셋 구조=>',dataset)

#3.학습용 데이터(train)의 첫번째 샘플을 확인
print("첫번째 샘플=>",dataset["train"][0])
'''
 train: Dataset({
        features: ['text', 'label'],
        num_rows: 8530
    })
    validation: Dataset({
        features: ['text', 'label'],
        num_rows: 1066
    })
    test: Dataset({
        features: ['text', 'label'],
        num_rows: 1066
    })
})
첫번째 샘플=> {'text': 'the rock is destined to be the 21st century\'s new " conan " and that he\'s going to make a splash even greater than arnold schwarzenegger , jean-claud van damme or steven segal .', 'label': 1}    

'''
