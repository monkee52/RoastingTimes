import tkinter
import tkinter.ttk
import tkinter.messagebox
import ctypes
import os
import webbrowser

def debug(msg):
    try:
        if __debug__:
            print("debug: %s" % msg)
    except:
        pass

# BEGIN HyperlinkManager
# Taken from http://effbot.org/zone/tkinter-text-hyperlink.htm
# Modified to use Label instead of Text
class HyperlinkManager:
    def __init__(self, text):
        self.text = text
        
        self.text.configure(foreground="blue")
        self.text.bind("<Enter>", self._enter)
        self.text.bind("<Leave>", self._leave)
        self.text.bind("<Button-1>", self._click)
    def add(self, action):
        self.action = action
    def _enter(self, ev):
        self.text.config(cursor="hand2")
    def _leave(self, ev):
        self.text.config(cursor="")
    def _click(self, ev):
        self.action(ev)
# END

class Object(object): #object type does not allow custom properties, but inherited classes do
    pass

class Intr(list): #quick way to print instructions
    def add(self, msg):
        self.append("%d. %s" % (self.__len__() + 1, msg))
    def get(self):
        return "\n".join(self)

class RoastingTimes:
    def geometry(self, width, height):
        #create user32
        user32 = ctypes.windll.user32
        
        #left and top coordinates for window
        x = (user32.GetSystemMetrics(0) - width) / 2
        y = (user32.GetSystemMetrics(1) - height) / 2

        return "%dx%d+%d+%d" % (width, height, x, y)
    
    def create(self):
        #create main window
        debug("creating main window")
        self.root = tkinter.Tk()
        self.root.title("Roasting Times Calculator")
        self.root.iconbitmap("%s%sRoastingTimes.ico" % (os.getcwd(), os.sep))
        self.root.geometry(self.geometry(353, 144))
        self.root.resizable(width = False, height = False)

        #create labels and widgets
        debug("settings variables for gui")
        self.text = RoastingTimesText(self)
        self.parts = RoastingTimesWidgets(self)

        #set font
        self.root.option_add("*Font", "Tahoma 8")

        self.parts.set_photo()

        debug("creating main Tkinter loop")
        self.root.mainloop()

    def ev_open_website(self, ev):
        webbrowser.open("http://www.roastingtimes.com/")

    def ev_meat_change(self, ev):
        #fired when user changes meat type
        meat = self.text.meatCombo.get()

        #beef, lamb or venison?
        if meat in self.text.meatValues[0:3]:
            self.parts.comboDoneness.configure(state="normal")
        else:
            self.parts.comboDoneness.configure(state="disabled")

        if meat in self.text.meatValues[0:6]: #beef, lamb, venison, pork, chicken, turkey
            self.parts.textWeight.configure(state="normal")
            self.parts.comboWeight.configure(state="normal")
        else: #i can't believe it's not beef, lamb, venison, pork, chicken, turkey
            self.parts.textWeight.configure(state="disabled")
            self.parts.comboWeight.configure(state="disabled")

        #change the photo to the relevant meat
        self.parts.set_photo()

    def lb_to_kg(self, lb):
        return lb * 0.45359242798

    def temps(self, celsius):
        fahrenheit = celsius * 9 / 5 + 32
        gas_mark = round(fahrenheit / 25 - 10) #round to remove unneccessary decimals, formula created in excel
        celsius = round(celsius)
        fahrenheit = round(fahrenheit)

        return "%d\xb0C (%d\xb0F, Gas Mark %d)" % (celsius, fahrenheit, gas_mark)

    def get_weight_multiplier(self, large, doneness):
        if large:
            if doneness == self.text.donenessValues[0]: #rare
                return 18
            elif doneness == self.text.donenessValues[1]: #medium
                return 24
            else: #well done
                return 36
        else:
            if doneness == self.text.donenessValues[0]: #rare
                return 20
            elif doneness == self.text.donenessValues[1]: #medium
                return 30
            else: #well done
                return 40
    
    def calculate_method(self, meat, weight = None, doneness = None):
        intrs = Intr()
        
        if weight == None: #everything but beef, lamb, venison, pork, chicken, turkey
            intrs.add("Preheat oven to %s." % (self.temps(220)))

            if meat == self.text.meatValues[6]: #pheasant
                intrs.add("Roast for 20 minutes at %s." % (self.temps(220)))
                intrs.add("Reduce oven temperature to %s and continue to roast for 30 to 40 minutes." % (self.temps(180)))
                intrs.add("Remove the joint from the oven and rest for 10 minutes before carving.")
            elif meat == self.text.meatValues[7]: #farmed duck
                intrs.add("Roast for 20 minutes at %s." % (self.temps(220)))
                intrs.add("Reduce oven temperature to %s and continue to roast for 60 to 90 minutes." % (self.temps(180)))
                intrs.add("Remove the joint from the oven and rest for 15 minutes before carving.")
            elif meat == self.text.meatValues[8]: #mallard duck
                intrs.add("Roast for 20 minutes at %s." % (self.temps(220)))
                intrs.add("Reduce oven temperature to %s and continue to roast for 35 to 45 minutes." % (self.temps(180)))
                intrs.add("Remove the joint from the oven and rest 10 minutes before carving.")
            else: #goose
                intrs.add("Roast for 20 minutes at %s." % (self.temps(220)))
                intrs.add("Reduce oven temperature to %s and continue to roast for 70 to 120 minutes." % (self.temps(180)))
                intrs.add("Remove the joint from the oven and rest for 20 to 30 minutes before carving.")
        elif doneness == None:
            if meat == self.text.meatValues[3]: #pork
                intrs.add("Preheat oven to %s." % (self.temps(220)))
                intrs.add("Roast for 30 minutes at %s." % (self.temps(220)))
                intrs.add("Reduce oven temperature to %s and continue to roast for %d minutes." % (self.temps(160), round(weight * 50)))
                intrs.add("Remove the joint from the oven and check that juices run clear.")
                intrs.add("Rest for 20 to 30 minutes before carving.")
            elif meat == self.text.meatValues[4]: #chicken
                intrs.add("Preheat oven to %s." % (self.temps(210)))
                intrs.add("Roast for 20 minutes at %s." % (self.temps(210)))
                intrs.add("Reduce oven temperature to %s and continue to roast for %d minutes." % (self.temps(180), 6.25 * weight + 32.5)) #formula created in excel
                intrs.add("Remove the joint from the oven and check that juices run clear.")
                intrs.add("Rest for 20 minutes before carving.")
            else: #turkey
                intrs.add("Preheat oven to %s." % (self.temps(220)))
                intrs.add("Roast for 20 minutes at %s." % (self.temps(230)))
                intrs.add("Reduce oven temperature to %s and continue to roast for %d minutes." % (self.temps(180), 11.765 * weight + 70.588)) #formula created in excel
                intrs.add("Remove the joint from the oven and check that juices run clear.")
                intrs.add("Rest for 20 to 30 minutes before carving.")
        else: #beef, lamb or venison
            intrs.add("Preheat oven to %s." % (self.temps(220)))
            
            if weight <= 5:
                intrs.add("Roast for 30 minutes at %s." % (self.temps(220)))

                multiplier = self.get_weight_multiplier(False, doneness)
                
                intrs.add("Reduce oven temperature to %s and continue to roast for %d minutes." % (self.temps(160), round(weight * multiplier)))
                intrs.add("Remove the joint from the oven and rest for 20 to 30 minutes before carving.")
            else:
                intrs.add("Roast for 40 minutes at %s." % (self.temps(220)))

                multiplier = self.get_weight_multiplier(True, doneness)

                intrs.add("Reduce oven temperature to %s and continue to roast for %d minutes." % (self.temps(160), round(weight * multiplier)))
                intrs.add("Remove the joint from the oven and rest for 30 minutes before carving.")
        self.show_method(meat, intrs.get())
    
    def ev_calculate(self, ev):
        #calculate the method for the selected meat, doneness and weight

        if self.validate_meat():
            meat = self.text.meatCombo.get()

            debug("meat is '" + meat + "'")

            if meat in self.text.meatValues[0:3]: #is the meat beef, lamb or venison?
                if self.validate_doneness(): #verify level of doneness is valid
                    doneness = self.text.donenessCombo.get()

                    debug("doneness is '" + doneness + "'")

                    if self.validate_weight(): #verify weight and measurement are valid
                        weight = float(self.text.weightValue.get())
                        measurement = self.text.weightCombo.get()

                        if measurement == self.text.weightValues[0]: #kg
                            debug("weight is '%d kg'" % (weight))
                            self.calculate_method(meat, weight, doneness)
                        else: #lb
                            new_weight = self.lb_to_kg(weight)
                            
                            debug("weight is '%d lb' or '%d kg'" % (weight, new_weight))
                            self.calculate_method(meat, new_weight, doneness)
            elif meat in self.text.meatValues[3:6]: #pork, chicken, turkey
                if self.validate_weight(): #verify weight and measurement are valid
                    weight = float(self.text.weightValue.get())
                    measurement = self.text.weightCombo.get()

                    if measurement == self.text.weightValues[0]: #kg
                        debug("weight is '%d kg'" % (weight))
                        self.calculate_method(meat, weight)
                    else: #lb
                        new_weight = self.lb_to_kg(weight)
                            
                        debug("weight is '%d lb' or '%d kg'" % (weight, new_weight))
                        self.calculate_method(meat, self.lb_to_kg(weight))
            else:
                self.calculate_method(meat)
                
    def validate_meat(self):
        meat = self.text.meatCombo.get()

        #make sure user entered a valid meat
        if meat in self.text.meatValues:
            return True
        
        debug("invalid meat")
        tkinter.messagebox.showwarning("Invalid input", "'" + meat + "' is not an available meat.")

        #select the default meat
        self.text.meatCombo.set(self.text.meatValues[0])
        self.parts.comboDoneness.configure(state="normal")
        self.parts.textWeight.configure(state="normal")
        self.parts.comboWeight.configure(state="normal")

        return False

    def validate_doneness(self):
        doneness = self.text.donenessCombo.get()
        
        #make sure user didn't add their own level of doneness
        if doneness in self.text.donenessValues:
            return True
        
        debug("invalid doneness")
        tkinter.messagebox.showwarning("Invalid input", "'" + doneness + "' is not an available level of doneness.")

        #set doneness to default value
        self.text.donenessCombo.set(self.text.donenessValues[0])

        return False

    def validate_weight(self):
        measurement = self.text.weightCombo.get()

        #make sure the units are valid
        if measurement in self.text.weightValues:
            weight = self.text.weightValue.get()

            #make sure the weight is actually a number
            try:
                tweight = float(weight)

                if tweight < 0 or tweight > 1134: #Large Continental breeds, such as Charolais, Marchigiana, Belgian Blue and Chianina
                    debug("invalid weight")
                    tkinter.messagebox.showwarning("Invalid input", "'" + weight + "' is either too large or too small (0 to 255).")

                    return False
                                
                return True
            except ValueError:
                debug("invalid weight")
                tkinter.messagebox.showwarning("Invalid input", "'" + weight + "' is a not a number.")

                #fill in default value
                self.text.weightValue.set("0")
                return False

        debug("invalid weight unit")
        tkinter.messagebox.showwarning("Invalid input", "'" + measurement + "' is not a compatible measurement.")

        #set unit to default value
        self.text.weightCombo.set(self.text.weightValues[0])

        return False
    
    def show_method(self, meat, methodtext):
        #create method window
        if hasattr(self, "method"):
           if self.method.root.winfo_exists():
               self.method.close()
        
        self.method = RoastingTimesMethod(self)
        self.method.open(meat, methodtext)
        
    def hide_method(self, p):
        self.method.close()

class RoastingTimesText:
    def __init__(self, root):
        #meat input
        debug("setting variables for meat")
        self.meatLabel = tkinter.StringVar(value="Meat: ")
        self.meatValues = ["Roast Beef", "Roast Lamb", "Roast Venison", "Roast Pork", "Roast Chicken", "Roast Turkey", "Roast Pheasant", "Roast Farmed Duck", "Roast Mallard Duck", "Roast Grouse", "Roast Goose"]
        self.meatImages = ["beef.ppm", "lamb.ppm", "venison.ppm", "pork.ppm", "chicken.ppm", "turkey.ppm", "pheasant.ppm", "farmedduck.ppm", "mallardduck.ppm", "grouse.ppm", "goose.ppm"]
        self.meatCombo = tkinter.StringVar(value=self.meatValues[0])

        #doneness input
        debug("setting variables for level of doneness")
        self.donenessLabel = tkinter.StringVar(value="Level of Doneness: ")
        self.donenessValues = ["Rare", "Medium", "Well-done"]
        self.donenessCombo = tkinter.StringVar(value=self.donenessValues[0])

        #weight input
        debug("setting variables for weight input")
        self.weightLabel = tkinter.StringVar(value="Weight: ")
        self.weightValues = ["kg", "lb"]
        self.weightCombo = tkinter.StringVar(value=self.weightValues[0])
        self.weightValue = tkinter.StringVar()

class RoastingTimesWidgets:
    def __init__(self, main):
        self.main = main
        self.root = self.main.root
        self.text = self.main.text

        #meat input
        debug("creating label for meat input")
        self.labelMeat = tkinter.ttk.Label(self.root)
        self.labelMeat.place(x=12, y=12, height=19, width=125)
        self.labelMeat.configure(textvariable=self.text.meatLabel)

        debug("creating combo box for meat input")
        self.comboMeat = tkinter.ttk.Combobox(self.root)
        self.comboMeat.place(x=137, y=10, height=23, width=140)
        self.comboMeat.configure(textvariable=self.text.meatCombo)
        self.comboMeat["values"] = self.text.meatValues
        self.comboMeat.bind("<<ComboboxSelected>>", lambda e: self.main.ev_meat_change(e))

        #doneness input
        debug("creating label for level of doneness input")
        self.labelDoneness = tkinter.ttk.Label(self.root)
        self.labelDoneness.place(x=12, y=45, height=19, width=125)
        self.labelDoneness.configure(textvariable=self.text.donenessLabel)

        debug("creating combo box for level of doneness input")
        self.comboDoneness = tkinter.ttk.Combobox(self.root)
        self.comboDoneness.place(x=137, y=43, height=23, width=140)
        self.comboDoneness.configure(textvariable=self.text.donenessCombo)
        self.comboDoneness["values"] = self.text.donenessValues

        #weight input
        debug("creating label for weight input")
        self.labelWeight = tkinter.ttk.Label(self.root)
        self.labelWeight.place(x=12, y=76, height=19, width=125)
        self.labelWeight.configure(textvariable=self.text.weightLabel)

        debug("creating text field for weight input")
        self.textWeight = tkinter.ttk.Entry(self.root)
        self.textWeight.place(x=137, y=74, height=23, width=140)
        self.textWeight.configure(textvariable=self.text.weightValue)

        debug("creating combo box for weight units")
        self.comboWeight = tkinter.ttk.Combobox(self.root)
        self.comboWeight.place(x=287, y=74, height=23, width=54)
        self.comboWeight.configure(textvariable=self.text.weightCombo)
        self.comboWeight["values"] = self.text.weightValues

        #calculate button
        debug("creating calculate button")
        self.buttonCalculate = tkinter.ttk.Button(self.root)
        self.buttonCalculate.place(x=261, y=107, height=25, width=80)
        self.buttonCalculate.configure(text="Calculate")
        self.buttonCalculate.bind("<Button-1>", lambda e: self.main.ev_calculate(e))

        #hyperlink to roasting times
        debug("creating hyperlink to website")
        self.linkWebsite = tkinter.Label(self.root)
        self.linkWebsite.place(x=12, y=110, height=19, width=243)
        self.linkWebsite.configure(text="www.RoastingTimes.com")

        hp_link = HyperlinkManager(self.linkWebsite)
        hp_link.add(self.main.ev_open_website)

        #image for those who dont know their meats
        debug("creating meat image")
        self.imageMeat = tkinter.ttk.Label(self.root)
        self.imageMeat.place(x=287, y=10, height=56, width=56)
    def set_photo(self):
        meat = self.text.meatCombo.get()
        index = self.text.meatValues.index(meat)
        image = "%s%simages%s%s" % (os.getcwd(), os.sep, os.sep, self.text.meatImages[index])

        debug("meat image: %s" % (image))

        photo = tkinter.PhotoImage(file=image)

        self.imageMeat.image = photo
        self.imageMeat.configure(image=self.imageMeat.image)

class RoastingTimesMethod:
    def __init__(self, master):
        self.master = master
        self.root = tkinter.Toplevel(self.master.root)
        self.root.iconbitmap("%s%sRoastingTimes.ico" % (os.getcwd(), os.sep))
        self.root.configure(padx=10, pady=10, takefocus=True)

        self.text = tkinter.StringVar()
        self._text = tkinter.ttk.Label(self.root)
        self._text.configure(textvariable=self.text)
        self._text.place(x=0, y=0, relwidth=1)
        self._text.pack()

        self.closeButton = tkinter.ttk.Button(self.root)
        self.closeButton.configure(text="Close")
        self.closeButton.place(y=10, width=107, height=25)
        self.closeButton.bind("<Button-1>", lambda e: self.close())
        self.closeButton.pack()
    def open(self, meat, text):
        self.root.title("Cooking instructions for %s" % meat)
        self.text.set(text)
        self._text.pack()
        self.closeButton.pack()
        
        #centre the window
        window_size = self.get_size()
        debug("method size is %dx%d" % window_size)
        self.root.geometry(self.master.geometry(window_size[0], window_size[1]))

        #focus and lock the window
        self.root.focus_set()
        self.root.grab_set()
        self.root.transient(self.master.root)
        self.root.wait_window(self.root)
    def get_size(self):
        self.root.update_idletasks()
        return tuple(int(x) for x in self.root.geometry().split("+")[0].split("x"))
    def close(self):
        self.root.destroy()

if __name__ == "__main__":
    rt = RoastingTimes()

    rt.create()
