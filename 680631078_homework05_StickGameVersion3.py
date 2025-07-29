# Stick Game Version 3
# bot จะเลือกหยิบไม้แบบฉลาดเพื่อให้ชนะเสมอ และรองรับจำนวนหยิบสูงสุดที่กำหนดได้
def smart_bot_move(stick_all, max_pick): #สร้างฟังก์ชั่นในการเลือกหยิบไม้ของ bot ที่ฉลาดในการเลือกหยิบให้ไดนะเสมอ
    """
    หาค่าที่ bot ควรหยิบเพื่อไม่ให้หยิบไม้แท่งสุดท้าย
    และพยายามทิ้งจำนวนไม้ให้ผู้เล่นอยู่ในจุดที่จะแพ้เสมอ (loseNumber) เช่น หากเลือกหยิบได้ [1,2] loseNumber=[1,4,7,10,...,ไปจนถึงใกล้stick_allมากที่สุด]
    """
    lose_nums = [(i * (max_pick + 1) + 1) for i in range(stick_all // (max_pick + 1) + 2)] #สูตรวิธีการคำนวณเลขให้ได้ loseNumber
    for i in range(1, max_pick + 1): #สร้างลูปให้จำนวนที่หยิบให้คนเล่นไปหา loseNumber 
        if (stick_all - i) in lose_nums: #ถ้าไท้กองรวม-i ที่อยู่ใน loseNumber จะคืนค่า i
            return i #คืนค่า i
    return min(max_pick, stick_all)  #ถ้าไม่มีทางชนะแน่ๆ ก็หยิบเท่าที่หยิบได้(เยอะสุด)

#รับตัวแปรต่างๆที่เกมต้องการ
stick_all = int(input("How many sticks (N) in the pile: ")) #รับตัวแปรจำนวนไม้ในกองทั้งหมด
max_pick = int(input("Maximum sticks you can pick at a time: ")) #รับจำนวนมากที่สุดที่จะเลือกหยิบได้ในแต่ละเทิร์น
name = input("What is your name: ") #รับตัวแปรชื่อผู้เล่น
count = 0 #กำหนดตัวแปรรอรับจำนวนครังที่เล่น
print(f"There are {stick_all} sticks in the pile.") #ให้แสดงเช็ตว่าไม้ในกองมีเท่าไหร่

# เริ่มเกม
while stick_all > 0: #ใช้ while loop เพื่อให้เล่นเกมจนกว่าไม้จะหมดกอง
    count += 1 #ให้บวก 1 ครั้งเรื่อย ๆ เมื่อมีการทาย
    #bot's turn เขียนให้เป็นตาเล่นของ bot เพื่อให้เข้าใจง่ายขึ้น
    if stick_all == 1: #กำหนดเงื่อนไขให้เมื่อกองไม้รวมเหลือ 1 จะต้องบังคับหยิบ
        bot = 1 #เลยกำหนดจำนวนไม้ bot เป็น 1 เลย
    else: #กรณีอื่น ๆ ให้เกมเล่นได้ต่อไป
        bot = smart_bot_move(stick_all, max_pick) #ให้ bot เลือกหยิบโดยใช้ฟังก์ชั่น smart_bot_move ที่เราตั้งค่าไว้
    stick_all -= bot #นำจำนวนกองไม้ทั้งหมดลบกับจำนวนที่ bot สุ่มหยิบ
    print(f"Bot picked {bot} stick(s). {stick_all} stick(s) remain.") #ให้แสดงว่า bot สุ่มหยิบไม้ไปจำนวนเท่าไหร่ และจะเหลือไม้ในกองเท่าไหร่
    if stick_all == 0: #กำหนดเงื่อนไขเมื่อกองไม้รวมเหลือ 0
        print("Bot picked the last stick. Bot loses!") #จะสั่งให้บอกว่า bot หยิบไม้ชิ้นสุดท้าย และ bot เป็นฝ่ายแพ้
        break #แล้วสั่งหยุด Loop
    print("-------------------") #ขั้นบรรทัดให้ดูง่ายขึ้นเฉยๆ

    #Player's turn ตาของผู้เล่นที่จะต้องทำการสุ่มหยิบ
    if stick_all == 1: #ถ้าเหลือ 1 ไม้ ต้องหยิบได้แค่ 1
        print("Only 1 stick left. You can only pick 1 stick.") #ให้แสดงว่าเหลือไม้ในกองแค่ 1 จะสามารถเลือกหยิบได้แค่ 1 เท่านั้น
        stick_rand = 1 #เลยกำหนดให้จำนวนไม้ที่หยิบเป็น 1 เสมอ
    else: #กรณีอื่น ๆ ให้เกมเล่นได้ต่อไป
        stick_rand = int(input(f"{name}, how many sticks will you take (1 to {min(max_pick, stick_all)}): ")) #รับตัวแปรจำนวนไม้ที่ผู้เล่นต้องการสุ่ม โดยจะเลือกหยิบได้ภายใน min(max_pick, stick_all)
        if stick_rand < 1 or stick_rand > min(max_pick, stick_all): #กำหนดเงือนไขถ้าจำนวนสุ่มหยิบน้อยกว่า 1 หรือมากกว่า min(max_pick, stick_all) จะผิดกฎและหยิบไม่ได้
            print("Invalid move! You can only take between 1 and", min(max_pick, stick_all))
            count -= 1 #ไม่นับรอบนี้เพราะถือว่าทำผิดกฎ
            continue #ให้ทำ loop ต่อ
    stick_all -= stick_rand #กำหนดให้เมื่อเข้าเงื่อนไขที่ถูกต้องในกานเลือกหยิบแล้ว ให้เอาจำนวนหยิบ-จำนวนกองทั้งหมด
    print(f"There are {stick_all} sticks in the pile.") #แจ้งให้ทราบว่าเหลือไม้ในกองเท่าไหร่
    if stick_all == 0: #กำหนดเงื่อนไขเมื่อกองไม้รวมเหลือ 0
        print(f"{name} picked the last stick. {name} loses!") #จะสั่งให้บอกว่า ผู้เล่น หยิบไม้ชิ้นสุดท้าย และผู้เล่นเป็นฝ่ายแพ้
        break #แล้วสั่งหยุด Loop
    print("-------------------") #ขั้นบรรทัดให้ดูง่ายขึ้นเฉยๆ

print("---------------------------") #ขั้นบรรทัดให้ดูง่ายขึ้นเฉยๆ
print(f"Okay, there is no stick left in the pile. Total turns: {count} times.") #ไม้หมดกองแล้วจึงแจ้งว่าไม่เหลือไม้แล้ว และบอกว่าบายไปทั้งหมดกี่รอบ