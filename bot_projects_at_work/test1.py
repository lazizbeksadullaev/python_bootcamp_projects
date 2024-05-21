# set1 = set()
# print('set1 = ', type(set1))
# # set2 = {}
# # print("set2 =", type(set2))
#
# set3 = {'a', 2, 4, 'sdfg', 3.4}
# print("set3 = ", set3)
# print("set3.add(9) = ", set3.add(9))
# print("set3.add('salom') = ", set3.add('salom'))
# print("set3 = ", set3)
# # set4 = set(i for i in range(10000, 1, -3))
# # print("set4 = ", set4)
# set3.remove('sdfg')# remove-olib tashlash
# print("set3.remove('sdfg') = ", set3)
# # set3.remove(5)# xatolik beradi
# set3.discard(5)
# set3.discard(4)
# print("set3.discard(4) = ", set3)
# for elt in set3: # to'plam bo'ylab kezib chiqish
#     print(elt)
# set3.add('Asaloy')
# set3.add('Dilshod')
# set3.add('Shohruh')
# set3.add('Sevinch')
# set3.add('Sevinch')
# set3.add('GULARO')
# print("set3 = ", set3)
# print('Gularo' in set3 or 'gularo' in set3 or 'Gularo'.upper() in set3)
#
# # Tuplamlar ustida amallar
# davomat1 = {'Shohruh', 'Asaloy', "Dilshod", "Gularo", "Madina", 'Yodgorbek'}
# davomat2 = {'Shohruh', 'Asaloy', "Dilshod", "Shohruh","Abdulla", "Madina", 'Sevinch'}
# # davomat = davomat1.union(davomat2)
# davomat = davomat1 | davomat2 # |-birlashtirish
# davomat = {'Shohruh', 'Asaloy', "Dilshod","Abdulla", "Madina", 'Sevinch', 'Shohruh', "Gularo", "Madina", 'Yodgorbek'}
# print("davomat = ", davomat)
# # davomat3 = davomat1.intersection(davomat2)
# davomat3 = davomat1 & davomat2 #  & - Tom  & Jarry
# print("davomat3 = ", davomat3)
# davomat5 = davomat1-davomat3
# print("davomat5 = ", davomat5)
#
# print(eval('2+3'))
# print('36'.isdigit())
# print('daftar'[:-1])
from math import factorial

# def calc(expr):
#     expr = list(expr)
#     new_expr = str()
#     son = str()
#
#     for i in range(len(expr)):
#         if expr[i] == '!':
#             new_expr += f'factorial({son})'
#             son = ''
#         elif expr[i] in "+-/*":
#             new_expr += son
#             new_expr += expr[i]
#             son = ''
#         else:
#             son += expr[i]
#     new_expr += son # buni ko'p xatolik olib keyin qo'ydim chunki ohirgi
#     # operatordan keyin yozilgan son new_expr ga qo'shilmay qolib ketar ekan
#     return new_expr

# print(calc('2+3*5!-4/4'))

# print(list('2+3*5-4/4'))
# print(eval('2+3*5-4/4'))

# bot.send_animation(message.chat.id, 'https://i.gifer.com/GEKm.mp4', duration=5)
#     with open(file='c:\\Users\\User\\Downloads\\Telegram Desktop\\CEO of Google photo_2022-10-07_14-03-25.jpg',
#               mode='rb') as photo:
#         bot.send_photo(message.chat.id, photo, 'google CEO')

t = int(input())
medium = []
for i in range(t):
    list1 = list(map(int, input().split()))
    list1.remove(max(list1))
    list1.remove(min((list1)))
    medium.extend(list1)
print(*medium, sep='\n')