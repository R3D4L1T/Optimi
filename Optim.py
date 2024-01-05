import flet as ft 
from pulp import LpMaximize, LpProblem, LpVariable, LpStatus, LpMinimize
import re

def extract_values(txt):
    values = re.findall(r'[-+]?\d*\.\d+|\d+', txt)
    return [float(val) for val in values]
    


def problem(val, prob, rest):
    print(val,prob, rest)
    # VALUES
    x = LpVariable(name = "x", lowBound=0, cat="Integer")
    y = LpVariable(name = "y", lowBound=0, cat="Integer")

    # PROBLEM
    problem = LpProblem()
    problem.sense=LpMaximize if prob[0]=="Maximize" else LpMinimize

    problem += float(prob[1]) * x + float(prob[2]) * y, "Utilidad_Total"

    # RESTRICTIONS
    for e in rest:
        if e[3] == '<=':
            problem += e[0] * x + e[1] * y  <= e[2], f"R_{e}"
            print('<=') 
        elif e[3] == '>=':
            problem += e[0] * x + e[1] * y  >= e[2], f"R_{e}" 
            print('<=') 
        elif e[3] == '=':
            problem += e[0] * x + e[1] * y  == e[2], f"R_{e}" 
        else:
            print('--------') 

    # SOLVE
    problem.solve()

    if problem.status == 1:
        anwr = 'Solution is optimal: %s' %LpStatus[problem.status]
        anwr += f'\nNumber of {val[0]} (X) = {x.varValue}'
        anwr += f'\nNumber of {val[1]} (Y) = {y.varValue}'
        return anwr
    else:
        return 'Failed to find solution: %s' %LpStatus[problem.status]



def main(page: ft.Page):
    page.title = "OPTIMI"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.window_resizable = False

    # --------->  Colors
    color_bg1 = "#2A2C39"
    color_bg2 = "#303445"
    color_TEXT = "#D9D277"
    color_text = "#C4D0F2"
    color_extra = "#F24452"

    dlg = ft.AlertDialog(
        title=ft.Text("only numbers!!!!"), on_dismiss=lambda e: print("Dialog dismissed!")
    )

    def add_restriction(e):
        
        try:
            float(x_res.value), float(Y_res.value), float(eq_res.value)
        except:
            page.dialog = dlg
            dlg.open = True
            page.update()
            return
        
        new_rest = f"-> {x_res.value}X + {Y_res.value}Y    {signal_res.value} {eq_res.value}"
        all_res.value += new_rest + "\n"

        x_res.value  = ""
        Y_res.value  = ""
        eq_res.value = ""
        page.update()

    def solve(e):
        
        try:
            float(x_target.value), float(y_target.value)

            val=[x_value.value, y_value.value]
            prob=[target.value, x_target.value, y_target.value]
            a = all_res.value.split("\n")
            a.pop()
            b= [(txt.split(' '))[7] for txt in a]
            a = [extract_values(ex) for ex in a]
            
            for i in range(len(a)):
                a[i].append(b[i])    

            solution = problem(val,prob,a)

            page.dialog = dlg
            dlg.title = ft.Text(solution)
            dlg.open = True
            page.update()

        except:
            page.dialog = dlg
            dlg.title = ft.Text("ERROR INPUT")
            dlg.open = True
            page.update()


    x_value = ft.TextField(label="X Description", focused_border_color=color_extra, hint_text="Please enter text here", color=color_text)
    y_value = ft.TextField(label="Y Description", focused_border_color=color_extra, color=color_text, hint_text="Please enter text here")

    cont_variables = ft.Container(        
        content=ft.Column(
            [
            ft.Row([
                ft.Container(
                    content=ft.Text("VARIABLE-X", style=ft.TextThemeStyle.TITLE_LARGE, text_align=ft.TextAlign.CENTER, color=color_TEXT),
                    width=200,  height=100,  padding=30
                    ),

                ft.Container(
                    content = x_value,
                    width=250,  height=100,  padding=30
                )
                
                ]
            ),

            ft.Row(
                controls=[
                ft.Container(
                    content=ft.Text("VARIABLE-Y", color=color_TEXT, style=ft.TextThemeStyle.TITLE_LARGE, text_align=ft.TextAlign.CENTER),
                    width=200,  height=100,   padding=2
                ),

                ft.Container(
                    content= y_value,
                    width=250, height=100, padding=1
                    )
                ],

                spacing= 30,
            )
            ]
        ),

        width=550,height=250,top=40,left=30,
        border_radius=ft.border_radius.all(20),
        padding=20,
        bgcolor=color_bg1,
        )


    target = ft.Dropdown(width=200,focused_border_color = color_extra,
                options=[
                    ft.dropdown.Option("Maximize"),
                    ft.dropdown.Option("Minimize"),
                ],)

    x_target = ft.TextField(label="X", color=color_text, focused_border_color=color_extra,  width=90, height=40)
    y_target = ft.TextField(label="Y", width=90, focused_border_color=color_extra, height=40, color=color_text)

    cont_target = ft.Container(
        content=ft.Column(
            controls=[
                ft.Text("---TARGET-----", size=16, color=color_TEXT, weight=ft.FontWeight.BOLD , text_align=ft.TextAlign.CENTER),

                target,

            ft.Container(
                content= ft.Row(
                    controls=[
                    x_target,
                    ft.Text(" X  +    ", size=16, color=color_text, weight=ft.FontWeight.BOLD , text_align=ft.TextAlign.CENTER),
                    y_target,
                    ft.Text(" Y   ", size=16, color=color_text, weight=ft.FontWeight.BOLD , text_align=ft.TextAlign.CENTER),
                    
                    ],
                    spacing=0
                ),
                bgcolor=color_bg2,
                width=350, height=100,padding=30, 
                border_radius=ft.border_radius.all(20)
                ),

            ],

            spacing=20,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        ),

        width=500, height=250,  top=40, left=50, padding=30,
        border_radius=ft.border_radius.all(20),
        bgcolor=color_bg1
        )

    x_res = ft.TextField(label="X", focused_border_color=color_extra, width=90, height=40)
    Y_res = ft.TextField(label="Y", width=90, height=40, focused_border_color=color_extra)
    eq_res = ft.TextField(label="Eq", color=color_text, focused_border_color=color_extra, width=90, height=40)
    
    signal_res = ft.Dropdown(width=60,focused_border_color= color_extra,
                             options=[ft.dropdown.Option(">="),ft.dropdown.Option("<="),ft.dropdown.Option(" ="),],
                             )

    all_res = ft.TextField(border = ft.border.all(1,color_extra), read_only=True, color=color_text,multiline=True,min_lines=1,max_lines=6,)

    cont_restrictions = ft.Container(
        
        content=ft.Column(
            [
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Text("  Restrictions", color=color_TEXT, style=ft.TextThemeStyle.TITLE_LARGE, text_align=ft.TextAlign.LEFT),
                            all_res                  
                        ],),

                    width=550,  height=220, padding=12,

                    ),

                ft.Container(
                content= ft.Row(
                    controls=[
                    x_res,
                    ft.Text(" X  + ", size=16, color=color_text, weight=ft.FontWeight.BOLD , text_align=ft.TextAlign.CENTER),
                    Y_res,
                    ft.Text(" Y   ", size=16, color=color_text, weight=ft.FontWeight.BOLD , text_align=ft.TextAlign.CENTER),
                    signal_res,
                    ft.Text("     ", size=16, color="white"),
                    eq_res,
                    ft.Text("   ", size=16, color="white"),
                    ft.ElevatedButton("ADD", on_click=add_restriction ,style=ft.ButtonStyle(shape=ft.ContinuousRectangleBorder(radius=30),),)
                    ],
                    spacing=0
                ),
                bgcolor=color_bg2,
                width=560, height=100,padding=10, 
                border_radius=ft.border_radius.all(20)
                ),
            ]    
        ),

        border_radius=ft.border_radius.all(20),
        width=650, top=7, left=7, height=350,
        bgcolor=color_bg1, padding=15
          
    )

    cont_buttons = ft.Container(
        content=ft.Row(
            controls=[
            ft.ElevatedButton("Clear all", icon="HIGHLIGHT_REMOVE"),
            ft.ElevatedButton("Solve", icon="CHECK_BOX", on_click=solve),
            ],
            spacing=120,
        ),
        
        bgcolor=color_bg1,
        border_radius=ft.border_radius.all(20),
        width=400, top=7, left=90, height=100, padding=30,
    )


    col1 = [
        ft.Stack([ft.Container(width=600, height=300), cont_variables]),
        ft.Stack([ft.Container( width=600, height=300), cont_target])
    ]

    col2 = [
        ft.Stack([ft.Container(width=600, height=400), cont_restrictions]),
        ft.Stack([ft.Container(width=600, height=150), cont_buttons])

    ]

    rowsP = [
        ft.Container(content=ft.Column(col1),  width=600, height=600),
        ft.Container(content=ft.Column(col2),  width=600, height=600)
    ]

    # Containers
    container_back = ft.Container(
        content=ft.Row(rowsP),
        margin=10,
        padding=1,
        alignment=ft.alignment.center,
        bgcolor=color_bg2,
        width=1300,
        height=700,
        border_radius=10,
    )

    page.add(container_back)


ft.app(target=main)

