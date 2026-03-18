
# ex7_str.py파일 작성

'''
문자열 String->순서를 갖는다.
'''
s='sequence'   # 문자열은 객체이다.
print(type(s)) # <class 'str'>
# ''.count() 객체를 사용하는 이유 => 1.데이터 저장(검증) typedDict 2.메서드호출=>객체명.메서드명(~)
print('길이(=크기):',len(s))    # 내장함수 => 8
print('포함횟수:',s.count('e')) # => 3
print('검색위치:',s.find('e'))  # 맨 첫번째만 찾아줌 => 1 
# s.find(찾을 문자열, 검색 시작위치 인덱스)
print('검색위치:',s.find('e'),s.find('e',3),s.rfind('e'))  # => 1 4 7
#첫글자 유무에 따라서 찾기(s로 시작,b로 시작)
print('첫글자 유무:',s.startswith('s'),s.startswith('b'))  # => True,False

#문자열은 수정이 안된다.
ss='mbc'
#mbc mbc 35129280
print(ss,'mbc',id(ss)) #mbc mbc 2110501788528

ss='abc'
print(ss,'mbc',id(ss)) #abc mbc 2110501399728

print('\nslicing')
#s='sequence' #[첫번째인수:마지막인수앞]
#[:마지막인수앞까지(0~)
#[첫번째인수:]->첫번째인수부터 끝까지 출력
#[::배수(n)]->0부터 배수(n)만큼 뽑아내라
#s='sequence'
print(s[0],s[2:4],s[:3],s[3:])#s qu seq uence
print(s[-1],s[-4:-1],s[-4:],s[::2])#e enc ence sqec
# -4부터 -2까지,-4부터 끝까지 
print('변경전',id(s))
s='fre'+s[2:]#quence
print(s)
print('변경후',id(s))#id값이 다르다.
print() #줄바꿈
s2='kbs mbc'
s2='  '+s2[:4]+'sbs'+s2[4:]
#  kbs sbsmbc
print(s2)
#  kbs sbsmbc
#앞뒤 공백제거->strip()

print(s2.strip())#양쪽 공백을 제거

print(s2.rstrip(),s2.lstrip())

#중간에 공백이 생기면->split()함수
s3=s2.split(sep=' ')#분리기호
print(s3)#문자열을 반환->리스트형태
#파이썬에서는 문자열을 취급->리스트,셋,튜플
# 문자열결합->join(문자열)
print(':'.join(s3))#::kbs:sbsmbc

#문자열을 변경
a='Life is too short'
print(id(a))
#replace(변경전단어,변경후 단어)
a=a.replace(a[:4], 'Your Leg')
print(a)

b=a.replace('Life','Your Leg')
print(b)
