import flet as ft
import os
import json
import functools

blue = '#A4BAB7'
black = '#080F0F'
red = '#720000'
dblue = '#94AEAA'









def main(page: ft.Page):
    page.title = "Workout app"
    page.horizontal_alignment = 'center'
    page.bgcolor = blue
    page.padding = 25
    page.auto_scroll = True
    page.scroll = ft.ScrollMode.HIDDEN
    
    page.fonts = {
        'Khand-Bold' : 'https://raw.githubusercontent.com/google/fonts/master/ofl/khand/Khand-Bold.ttf',
        'Khand-Reg' : 'https://raw.githubusercontent.com/google/fonts/master/ofl/khand/Khand-Regular.ttf'
        
    }
    
    
    def delete(e, name):
            with open("data.json", 'r') as data:
                dict = json.load(data)
                print(dict)
            index = dict["index"][name]

            dict["workouts"].pop(index)
            dict["day"].pop(index)
            dict["max"].pop(index)
            dict["index"].pop(name)

            for exercise_name, exercise_index in dict["index"].items():
                if exercise_index > index:
                    dict["index"][exercise_name] = exercise_index - 1

            with open("data.json", 'w') as data:
                json.dump(dict, data)
            
            print(name)
            page_1(e)
    
    def all_add():
        with open('data.json', 'r') as data:
                dict = json.load(data)
            
        singles = []
            
        for i in dict["workouts"]:
                name = i
                max = dict["max"][dict["index"][name]]
                day = dict["day"][dict["index"][name]]
                singles.append(workoutOne(name, max, day))
        return singles
    
    def count_reps(max, day):
        first = int((max - 0.4*max)//1) + day - 1
        second = int((first - 1)//1)
        third = int((second -1)//1)
        fourth = int((third)//1)
        fivth = int((third - 1)//1)
        return [first, second, third, fourth, fivth]
        
    def workoutOne(name , max, day):
        listik = count_reps(max, day)
        
        first = listik[0]
        second = listik[1]
        third = listik[2]
        fourth = listik[3]
        fivth = listik[4]
        
        single = ft.Container(
            height = 65,
            bgcolor = dblue,
            padding = 10,
            border = ft.border.all(2, red),
            border_radius = 10,
            content = ft.Row(
                [   #name
                    ft.TextButton(
                        content = ft.Text(name.title(), size = 24, font_family='Khand-Reg', color = black),
                        on_click= lambda e: page_3(e, name)),
                    
                    #repetitions
                    ft.Row(
                        [
                            ft.Text(first, size = 24, font_family='Khand-Reg', color = black),
                            ft.Text(second, size = 24, font_family='Khand-Reg', color = black),
                            ft.Text(third, size = 24, font_family='Khand-Reg', color = black),
                            ft.Text(fourth, size = 24, font_family='Khand-Reg', color = black),
                            ft.Text(fivth, size = 24, font_family='Khand-Reg', color = black),
                        ]
                    ),
                    
                    #del
                    ft.Container(
                        border_radius = 1,
                        width = 55,
                        content = ft.TextButton(
                            on_click = lambda e: delete(e, name),
                            content = ft.Text('DEL', color = red, font_family='Khand-Reg', size = 24)
                            )
                    )
                    
                ], alignment = ft.MainAxisAlignment.SPACE_BETWEEN,
            )
            
        ) 
        return single
    
    #delete
    
    
    #success banner
    def success():
        def close_banner(e):
            page.banner.open = False
            page.update()
            page_1(e)

        page.banner = ft.Banner(
            bgcolor=ft.colors.GREEN_200,
            content=ft.Text(
                value = "Workout is added successfully!",
                font_family="Khand-Reg",
                color = black
            ),
            actions=[
                ft.TextButton(content = ft.Text(
                    value = "Go to the main page",
                    font_family="Khand-Reg",
                    color = black
                    ), on_click=close_banner),
            ],
        ) 
        page.banner.open = True
        page.update()
    
    #submit
    def submit(name, max):
        def close_banner(e):
            page.banner.open = False
            page.update()

        page.banner = ft.Banner(
            bgcolor=ft.colors.AMBER_100,
            leading=ft.Icon(ft.icons.WARNING_AMBER_ROUNDED, color=ft.colors.AMBER, size=40),
            content=ft.Text(
                value = "This name is already used or your max contains a letter(s)!",
                font_family="Khand-Reg",
                color = black
            ),
            actions=[
                ft.TextButton("Okey", on_click=close_banner),
            ],
        ) 
        
        with open('data.json', 'r') as data:
            dict = json.load(data)
        if name in dict["workouts"]:
            page.banner.open = True
            page.update()
        else:
            try:
                dict["max"].append(int(max))
                dict["workouts"].append(name)
                dict["day"].append(1)
                dict["index"][name] = len(dict["workouts"])-1
                
                with open('data.json', 'w') as data:
                    json.dump(dict, data)
                success()
            except:
                page.banner.open = True
                page.update()
        
    
    #page 1
    def page_1(e):
        page.clean()
        title = ft.Container(
            margin = 100,
            content = ft.Row(
                [ft.Text(
                    value = 'Wellcome!', 
                    color = black, 
                    font_family='Khand-Bold', 
                    text_align='center', 
                    size = 48)], 
                alignment=ft.MainAxisAlignment.CENTER,))
        
        
        
        workouts = ft.Column(
            [
            #your workouts
            ft.Container(
                content = ft.Row(
                    [ft.Text(value = 'Your workouts', color = black, font_family = 'Khand-Reg', text_align = 'left', size = 24)],
                    alignment = ft.MainAxisAlignment.START)
            ),
            
            ft.Column(all_add())
            ]
        )
        page.clean()
        page.add(title, workouts)
    
    #page 2 (new exercise)
    def page_2(e):
        
        def givevalueName(e):
            name.value = e.control.value
            page.update()
            
        def givevalueMax(e):
            max_rep.value = e.control.value
            page.update()
        
        name = ft.Text(value = "Untitled")
        max_rep = ft.Text(value = "20")
        
        title = ft.Container(
            margin = 70,
            content = ft.Row(
                [ft.Text(
                    value = 'New exerecise', 
                    color = black, 
                    font_family='Khand-Bold', 
                    text_align='center', 
                    size = 40)], 
                alignment=ft.MainAxisAlignment.CENTER,))

        form = ft.Row([
            ft.Column(
            [   
                ft.Text(
                    value = "Exercise's name",
                    color = black,
                    font_family = "Khand-Reg",
                    size = 20
                ),
                
                ft.TextField(
                    value = 'Untitled',
                    color = black,
                    bgcolor=dblue,
                    width = 318,
                    height = 40,
                    content_padding=5,
                    border_color=red,
                    border_width=2,
                    on_change=givevalueName
                    ),
                
                
                ft.Text(
                    value = "Max repetitions",
                    color = black,
                    font_family = "Khand-Reg",
                    size = 20,
                    ),
                
                
                
                ft.Row(
                    [
                        ft.TextField(
                            value = '20',
                            color = black,
                            bgcolor = dblue,
                            width = 76,
                            height = 40,
                            content_padding = 0,
                            text_align='center',
                            border_color=red,
                            border_width=2,
                            on_change=givevalueMax
                            ),
                        
                        
                        ft.TextButton(content = ft.Text(
                            value = "Cencel",
                            font_family='Khand-Bold',
                            size = 20,
                            color=black
                            ), on_click=page_1),
                        
                        ft.TextButton(content = ft.Text(
                            value = "Submit",
                            font_family='Khand-Bold',
                            size = 20,
                            color=black
                            ), on_click=lambda e: submit(name.value, max_rep.value))
                    ]
                )
                ])
        ], alignment=ft.MainAxisAlignment.CENTER)     
                
        page.clean()
        page.add(title, form)
        
    count = ft.Text(value = "0")
    
    #page 3 
    def page_3(e, name): 
        with open('data.json', 'r') as data:
            dict = json.load(data) 
        index = dict["index"][name]
        title = name
        max = dict["max"][index]
        day = dict["day"][index]

        listik = count_reps(max, day)
        
        first = listik[0]
        second = listik[1]
        third = listik[2]
        fourth = listik[3]
        fivth = listik[4]
        
        reps = [first, second, third, fourth, fivth]
        
        current = reps[int(count.value)]
        
        #next current
        def  change_current(e):
            if int(count.value) == 4:
                count.value = 0
                with open("data.json", "r") as data:
                    dict = json.load(data)
                
                dict["day"][dict["index"][name]] += 1  
                
                with open("data.json", "w") as data:
                    json.dump(dict, data)
                page_1(e)
            else:
                count.value = str( int(count.value) + 1)
                page_3(e, name)
        
        title = ft.Container(
            margin = 40,
            content = ft.Row([
            ft.Text(value = name, font_family="Khand-Bold", size = 48),
            ft.Text(value = "day "+ str(day), font_family="Khand-Bold", size = 48)
        ], alignment=ft.MainAxisAlignment.CENTER))
        
        body = ft.Column(
            [  
             ft.Row([ft.Text(
                 value= "Try your best!",
                 size = 40, 
                 font_family= 'Khand-Reg',
                 text_align="center"
             )], alignment=ft.MainAxisAlignment.CENTER),
             
                 
            ft.Row([ft.Container(
                padding = 33,
                width = 150,
                height= 150,
                bgcolor= dblue,
                border= ft.border.all(2, red),
                border_radius = 15,
                content = ft.Text(value = current, font_family='Khand-Bold', size = 64, text_align= "center")
                 )], alignment=ft.MainAxisAlignment.CENTER),
            
            ft.Row([ft.TextButton(
                content = ft.Text(
                    value = "Done",
                    size = 40,
                    font_family= "Khand-Reg",
                    color = black
                ),
                on_click= change_current
                )], alignment = ft.MainAxisAlignment.CENTER)
            ]
        )
        
        page.clean()
        page.add(title, body)
    
    
    
    
    
    title = ft.Container(
        margin = 100,
        content = ft.Row(
            [ft.Text(
                value = 'Wellcome!', 
                color = black, 
                font_family='Khand-Bold', 
                text_align='center', 
                size = 48)], 
            alignment=ft.MainAxisAlignment.CENTER,))
    
    
    
    workouts = ft.Column(
        [
        #your workouts
        ft.Container(
            content = ft.Row(
                [ft.Text(value = 'Your workouts', color = black, font_family = 'Khand-Reg', text_align = 'left', size = 24)
                ],
                alignment = ft.MainAxisAlignment.START)
        ),
        
        ft.Column(all_add()),
            
        ]
    )
    
    page.floating_action_button = ft.FloatingActionButton(
        content=ft.Icon(ft.icons.ADD, color = black),
        bgcolor=dblue,
        width=55,
        on_click = page_2
    )
    
    page.add(title, workouts)
    
    

    
    
ft.app(target=main)