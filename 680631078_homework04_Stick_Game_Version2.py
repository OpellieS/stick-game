#Stick game version 2
#โดยจะเพิ่มให้ AL เข้ามาเล่นกับเราด้วย โดยสุ่มแค่ 1-2 ไม้
import random as rd #ดึงฟังก์ชันสุ่มมาใช้ สำหรับในการสุ่มหยิบไม้ของ bot
stick_all = int(input ("How many sticks (N) in the pile: ")) #รับตัวแปรจำนวนไม้ในกองทั้งหมด
name = input("What is your name: ") #รับตัวแปรชื่อผู้เล่น
count = 0 #กำหนดตัวแปรรอรับจำนวนครังที่เล่น
print(f"There are {stick_all} sticks in the pile.") #ให้แสดงเช็ตว่าไม้ในกองมีเท่าไหร่

while stick_all > 0: #ใช้ while loop เพื่อให้เล่นเกมจนกว่าไม้จะหมดกอง
    count += 1 #ให้บวก 1 ครั้งเรื่อย ๆ เมื่อมีการทาย
    #bot's turn เขียนให้เป็นตาเล่นของ bot เพื่อให้เข้าใจง่ายขึ้น
    if stick_all ==1: #กำหนดเงื่อนไขให้เมื่อกองไม้รวมเหลือ 1 จะต้องบังคับหยิบ
        bot=1 #เลยกำหนดจำนวนไม้ bot เป็น 1 เลย
    else:
        bot=rd. randint(1,min(2,stick_all)) #กำหนดตัวแปร bot มา โดยจะให้ bot สุ่มหยิบจำนวน 1-2 ไม้
    stick_all -= bot #นำจำนวนกองไม้ทั้งหมดลบกับจำนวนที่ bot สุ่มหยิบ
    print (f"Bot have pick {bot} stick and now have {stick_all} in the pile") #ให้แสดงว่า bot สุ่มหยิบไม้ไปจำนวนเท่าไหร่ และจะเหลือไม้ในกองเท่าไหร่
    if stick_all ==0: #กำหนดเงื่อนไขเมื่อกองไม้รวมเหลือ 0
        print (f"Bot pick last stick, Bot lose!") #จะสั่งให้บอกว่า bot หยิบไม้ชิ้นสุดท้าย และ bot เป็นฝ่ายแพ้
        break #แล้วสั่งหยุด Loop
    print("--------------") #ขั้นบรรทัดให้ดูง่ายขึ้นเฉยๆ
    #Player's turn ตาของผู้เล่นที่จะต้องทำการสุ่มหยิบ
    if stick_all == 1: # ถ้าเหลือ 1 ไม้ ต้องหยิบได้แค่ 1
        print ("Only 1 stick left. You can take only 1 stick.") #แจ้งเตือนว่าเหลือไม้ในกองแค่ 1 จะสามารถเลือกหยิบได้แค่ 1 เท่านั้น
        stick_rand = 1 #เลยกำหนดให้จำนวนไม้ที่หยิบเป็น 1 เสมอ
    else: #กรณีอื่นทั้งหมดที่ไม้ในกองไม่เป็น 1
        stick_rand = int(input(f"{name}, how many sticks will you take (1 or 2) : ")) #รับตัวแปรจำนวนไม้ที่ผู้เล่นต้องการสุ่ม
        if stick_rand not in [1, 2]: #กำหนดเงือนไขถ้าจำนวนสุ่มหยิบไม่ใช่ 1,2 จะผิดกฎและหยิบไม่ได้
            print("No! You can only take 1 or 2 sticks!") #บอกว่าสามารถหยิบได้แค่ 1,2 ไม้เท่านั้น
            count -= 1 # ไม่นับรอบนี้เพราะถือว่าทำผิดกฎ
            continue #ให้ทำ loop ต่อ
    stick_all -= stick_rand #กำหนดให้เมื่อเข้าเงื่อนไขที่ถูกต้องในกานเลือกหยิบแล้ว ให้เอาจำนวนหยิบ-จำนวนกองทั้งหมด
    print(f"There are {stick_all} sticks in the pile.") #แจ้งให้ทราบว่าเหลือไม้ในกองเท่าไหร่
    if stick_all == 0: #กำหนดเงื่อนไขเมื่อกองไม้รวมเหลือ 0
        print(f"{name} pick last stick, {name} lose!") #จะสั่งให้บอกว่า ผู้เล่น หยิบไม้ชิ้นสุดท้าย และ ผู้เล่น เป็นฝ่ายแพ้
        break
    print("-----------------") #ขั้นบรรทัดให้ดูง่ายขึ้นเฉยๆ
print("------------------") #ขั้นบรรทัดให้ดูง่ายขึ้นเฉยๆ
print(f"Okay, there is no stick left in the pile.Total turns: {count} times.") #ไม้หมดกองแล้วจึงแจ้งว่าไม่เหลือไม้แล้ว และบ