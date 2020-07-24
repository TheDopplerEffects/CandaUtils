
app = gui()
progress = 0
def addbar():
    pass
    
def update():
    global progress 
    progress = app.getEntry('1')
    if progress is None:
        progress = 0
    app.setMeter('progress', progress)
    
#class valbox(object):
#    def __init__(self, Stream = None, )
    
def press(name):
    if name == 'Exit':
        app.stop()
    else: 
        try:
            firstnum = int(app.getEntry('first'))
            secondNum = int(app.getEntry('sn'))
    
            message = 'The results are as fallows \n\n'
            message += 'add' + str(firstnum + secondNum) + '\n'
    
            if name == 'Result':
                app.setLabel('result', message)
            elif name == 'MessageBox Redult':
                app.infoBox('Result', message)
    
        except ValueError as e:
            app.errorBox('Error', 'Invalid Number')
            app.setFocus('first') 
    
app.addNumericEntry('1')
app.addMeter('progress')
app.setMeterFill('progress', 'blue')
app.setMeter('progress', progress)
    
app.registerEvent(update)
    
    
    
app.go()
