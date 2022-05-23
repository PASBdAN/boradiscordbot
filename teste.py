def function(a:int, b:int):
    return a + b

def soma_2_e_5(func):
    return func

print(soma_2_e_5(lambda x,y: x+y)(2,5))


from datetime import datetime, timezone, timedelta

def dia_tarde_noite():
    timezone_offset = -3.0  # Pacific Standard Time (UTC−03:00)
    tzinfo = timezone(timedelta(hours=timezone_offset))
    hour = int(datetime.now(tzinfo).hour)
    if hour >= 5 and hour < 12:
        return "bom dia"
    elif hour >= 12 and hour < 18:
        return "boa tarde"
    else:
        return "boa noite"

print(dia_tarde_noite())