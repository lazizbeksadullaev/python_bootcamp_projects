# # list_tasks_9
#
# qatorlar = 0
# suzlar = 0
# belgilar = 0
# with open('c:\\Users\\User\\PycharmProjects\\New_Text.txt','r') as file:
#     print("file = ", file)
#     for i in file:
#         qatorlar += 1
#         suzlar += len(i.split())
#         belgilar += len(i.strip('\n'))
# print('qatorlar soni = ', qatorlar)
# print('sozlar soni = ', suzlar)
# print('belgilar soni = ', belgilar)


# with open('c:\\Users\\User\\PycharmProjects\\New_Text.txt','w') as file:
#     for i in range(1,10):
#         for j in range(1,10):
#             file.write(f"{i}*{j} = {i*j}\n")
#             # print(i, '*', j, '=', i * j, end='\n')
#         file.write('\n')
#         # print('\t')

# list1 = list(map(int, input().split()))
# print("list1 = ", list1)
# qatnashish ={}
#
# for i in list1:
#     qatnashish[i] = list1.count(i)
#
#
# k = 0
# ohirgi = int()
# for key,value in qatnashish.items():
#     if value >= k:
#         k = value
#         ohirgi = key
#
# print(ohirgi)

#
#
# try:
#     print('0.'+input().split('.')[1])
# except:
#     print('0')


# ruyxat = [[1,2,3], [4,5,6], [7,8,9]]
#
# for i in range(len(ruyxat)):
#     for j in range(len(ruyxat)):
#         if j <= i:
#             print(ruyxat[i][j], end=' ')
#     print()