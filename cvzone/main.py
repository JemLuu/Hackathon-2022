import time

import cv2
import keyboard

import cvzone
import PySimpleGUI as sg
from cvzone.FaceMeshModule import FaceMeshDetector
from cvzone.PlotModule import LivePlot


class Eye:

    
    @staticmethod
    def showBoth():
        startTime = time.perf_counter()
        capture = cv2.VideoCapture(0)
        detector = FaceMeshDetector(maxFaces=1)
        plotY = LivePlot(694, 520, [18,37])

        idList = [22, 23, 24, 26, 110, 130, 157, 158, 159, 160, 161, 243]
        blinkCounter = 0
        timer = 0
        
        start = time.perf_counter()
        blinking = 0
        blinkTimer = 0
        blinkTracker = [0.12]*90
        avgBlinks = 0

        while not (keyboard.is_pressed('x')):
            success, img = capture.read()
            img, faces = detector.findFaceMesh(img, draw = False)

            if faces:
                face = faces[0]
                #for id in idList:
                #    cv2.circle(img, face[id], 5, (255, 0, 255), cv2.FILLED)

                leftUp = face[159]
                leftDown = face[23]
                leftLeft = face[130]
                leftRight = face[243]

                lengthHor = detector.findDistance(leftUp, leftDown)
                lengthVer = detector.findDistance(leftLeft, leftRight)

                #cv2.line(img, leftUp, leftDown, (0, 200, 0), 3)
                #cv2.line(img, leftLeft, leftRight, (0, 200, 0), 3)

                ratio = (int)(lengthVer[0]/lengthHor[0]*10)
                if ratio > 27 and timer == 0:
                    blinkCounter += 1
                    timer = 1
                if timer != 0:
                    timer += 1
                    if timer > 8:
                        timer = 0

                if ratio > 27:
                    blinking = 1
                    blinkTimer = 1
                if blinkTimer != 0:
                    blinkTimer += 1
                    if blinkTimer > 5:
                        blinkTimer = 0
                        blinking = 0

                currentTime = time.perf_counter()
                timeIndex = (int)(((currentTime - start)*3 % 90))
                blinkTracker[timeIndex] = blinking
                avgBlinks = (int)(sum(blinkTracker))
                

                if (avgBlinks < 5):
                    cvzone.putTextRect(img, 'NEED TO BLINK MORE', (64,255), 3, 3, (255, 255, 255), (34,139,34))
                #if avgBlinks below some threshold send warning message as a pop-up

                cvzone.putTextRect(img, f'Average BPM: {avgBlinks}', (0,45), 3, 3, (255, 255, 255), (34,139,34))
                cvzone.putTextRect(img, f'Total Blinks: {blinkCounter}', (0,90), 2, 3, (255, 255, 255), (34,139,34))
                imgPlot = plotY.update(ratio)
                img = cv2.resize(img, (694, 520))
                combo = cvzone.stackImages([img, imgPlot], 2, 0.8)

            else:
                cvzone.putTextRect(img, 'No Face Detected', (170,240), 2, 3, (255, 255, 255), (34,139,34))
                imgPlot = plotY.update(23)
                img = cv2.resize(img, (694, 520))
                combo = cvzone.stackImages([img, imgPlot], 2, 0.8)

            img = cv2.resize(img, (694, 520))
            cv2.imshow("Eye Tracker", combo)
            cv2.waitKey(1)

        capture.release()
        cv2.destroyAllWindows()
        endTime = time.perf_counter()
        
        return blinkCounter, (endTime-startTime)
    

    @staticmethod
    def startVideo():
        startTime = time.perf_counter()
        capture = cv2.VideoCapture(0)
        detector = FaceMeshDetector(maxFaces=1)

        idList = [22, 23, 24, 26, 110, 130, 157, 158, 159, 160, 161, 243]
        blinkCounter = 0
        timer = 0
        
        start = time.perf_counter()
        blinking = 0
        blinkTimer = 0
        blinkTracker = [0.12]*90
        avgBlinks = 0

        while not (keyboard.is_pressed('x')):
            success, img = capture.read()
            img, faces = detector.findFaceMesh(img, draw = False)

            if faces:
                face = faces[0]
                #for id in idList:
                #    cv2.circle(img, face[id], 5, (255, 0, 255), cv2.FILLED)

                leftUp = face[159]
                leftDown = face[23]
                leftLeft = face[130]
                leftRight = face[243]

                lengthHor = detector.findDistance(leftUp, leftDown)
                lengthVer = detector.findDistance(leftLeft, leftRight)

                #cv2.line(img, leftUp, leftDown, (0, 200, 0), 3)
                #cv2.line(img, leftLeft, leftRight, (0, 200, 0), 3)

                ratio = (int)(lengthVer[0]/lengthHor[0]*10)
                if ratio > 27 and timer == 0:
                    blinkCounter += 1
                    timer = 1
                if timer != 0:
                    timer += 1
                    if timer > 8:
                        timer = 0

                if ratio > 27:
                    blinking = 1
                    blinkTimer = 1
                if blinkTimer != 0:
                    blinkTimer += 1
                    if blinkTimer > 5:
                        blinkTimer = 0
                        blinking = 0

                currentTime = time.perf_counter()
                timeIndex = (int)(((currentTime - start)*3 % 90))
                blinkTracker[timeIndex] = blinking
                avgBlinks = (int)(sum(blinkTracker))
                

                if (avgBlinks < 5):
                    cvzone.putTextRect(img, 'NEED TO BLINK MORE', (64,255), 3, 3, (255, 255, 255), (34,139,34))
                #if avgBlinks below some threshold send warning message as a pop-up

                cvzone.putTextRect(img, f'Average BPM: {avgBlinks}', (0,45), 3, 3, (255, 255, 255), (34,139,34))
                cvzone.putTextRect(img, f'Total Blinks: {blinkCounter}', (0,90), 2, 3, (255, 255, 255), (34,139,34))
            else:
                cvzone.putTextRect(img, 'No Face Detected', (170,240), 2, 3, (255, 255, 255), (34,139,34))

            img = cv2.resize(img, (694, 520))
            cv2.imshow("Eye Tracker", img)
            cv2.waitKey(1)

        capture.release()
        cv2.destroyAllWindows()
        
        endTime = time.perf_counter()
        return blinkCounter, (endTime-startTime)


    @staticmethod
    def plot():
        capture = cv2.VideoCapture(0)
        detector = FaceMeshDetector(maxFaces=1)
        plotY = LivePlot(640, 360, [18,37])

        while not (keyboard.is_pressed('x')):
            success, img = capture.read()
            img, faces = detector.findFaceMesh(img, draw = False)

            if faces:
                face = faces[0]

                leftUp = face[159]
                leftDown = face[23]
                leftLeft = face[130]
                leftRight = face[243]

                lengthHor = detector.findDistance(leftUp, leftDown)
                lengthVer = detector.findDistance(leftLeft, leftRight)

                ratio = (int)(lengthVer[0]/lengthHor[0]*10)
               
                imgPlot = plotY.update(ratio)
            else:
                imgPlot = plotY.update(23)

            cv2.imshow("Blink Plot", imgPlot)
            cv2.waitKey(1)

        capture.release()
        cv2.destroyAllWindows()



    @staticmethod
    def showStats():
        startTime = time.perf_counter()
        capture = cv2.VideoCapture(0)
        white = cv2.VideoCapture(r"C:\Users\jc803\OneDrive\Desktop\cvzone\videoplayback.mp4")
        detector = FaceMeshDetector(maxFaces=1)

        idList = [22, 23, 24, 26, 110, 130, 157, 158, 159, 160, 161, 243]
        blinkCounter = 0
        timer = 0
        
        start = time.perf_counter()
        blinking = 0
        blinkTimer = 0
        blinkTracker = [0.12]*90
        avgBlinks = 0

        while not (keyboard.is_pressed('x')):

            if (white.get(cv2.CAP_PROP_POS_FRAMES) == white.get(cv2.CAP_PROP_FRAME_COUNT)):
                white.set(cv2.CAP_PROP_POS_FRAMES, 0)

            success, whiteIMG = white.read()

            success, img = capture.read()
            img, faces = detector.findFaceMesh(img, draw = False)

            if faces:
                face = faces[0]
                #for id in idList:
                #    cv2.circle(img, face[id], 5, (255, 0, 255), cv2.FILLED)

                leftUp = face[159]
                leftDown = face[23]
                leftLeft = face[130]
                leftRight = face[243]

                lengthHor = detector.findDistance(leftUp, leftDown)
                lengthVer = detector.findDistance(leftLeft, leftRight)

                #cv2.line(img, leftUp, leftDown, (0, 200, 0), 3)
                #cv2.line(img, leftLeft, leftRight, (0, 200, 0), 3)

                ratio = (int)(lengthVer[0]/lengthHor[0]*10)
                if ratio > 27 and timer == 0:
                    blinkCounter += 1
                    timer = 1
                if timer != 0:
                    timer += 1
                    if timer > 8:
                        timer = 0

                if ratio > 27:
                    blinking = 1
                    blinkTimer = 1
                if blinkTimer != 0:
                    blinkTimer += 1
                    if blinkTimer > 5:
                        blinkTimer = 0
                        blinking = 0

                currentTime = time.perf_counter()
                timeIndex = (int)(((currentTime - start)*3 % 90))
                blinkTracker[timeIndex] = blinking
                avgBlinks = (int)(sum(blinkTracker))
                
                whiteIMG = cv2.resize(whiteIMG, (420, 300))

                if (avgBlinks < 5):
                    cvzone.putTextRect(whiteIMG, 'NEED TO BLINK MORE', (37, 170), 2, 3, (255, 255, 255), (34,139,34))
                

                cvzone.putTextRect(whiteIMG, f'Average BPM: {avgBlinks}', (5,55), 3, 3, (255, 255, 255), (34,139,34))
                cvzone.putTextRect(whiteIMG, f'Total Blinks: {blinkCounter}', (80,100), 2, 3, (255, 255, 255), (34,139,34))
            else:
                whiteIMG = cv2.resize(whiteIMG, (420, 300))
                cvzone.putTextRect(whiteIMG, 'No Face Detected', (57,140), 2, 3, (255, 255, 255), (34,139,34))

            whiteIMG = cv2.resize(whiteIMG, (420, 300))
            cv2.imshow("Eye Tracker", whiteIMG)
            cv2.waitKey(1)

        capture.release()
        cv2.destroyAllWindows()
        endTime = time.perf_counter()
        return blinkCounter, (endTime - startTime)
    




def main():
    sg.theme('DarkGreen5')
    f = "Georgia"
    font = (f, 20, 'bold')
    font2 = (f, 15, 'bold')
    font3 = (f, 35, 'bold')
    font4 = (f, 30, 'bold')
    dataFile = open("data.txt", 'a')

    sg.set_options(font=font)
    layout = [  [sg.Text("Blink Tracker with Reminders to Blink", font = font3, text_color = "White", background_color = "SteelBlue4")],
                [sg.Text("                                Created by: Jon Coulter, Jeremy Luu, and Kameren Jouhal", font = font2)],
                [sg.Text("\n")],
                [sg.Button('Track Blinks', font = (font4), size = (12,1)), sg.Text("                        (Press 'x' to close windows)")],
                [sg.Text("\n")],
                [sg.Button('Blink Graph', font = (font4), size = (12,1))], 
                [sg.Text("\n")],
                [sg.Button('Track & Graph', font = (font4), size = (12,1))],
                [sg.Text("\n")],
                [sg.Button('Text Tracker', font = (font4), size = (12,1)), sg.Text("                            "), sg.Button('Exit', font = (font4), size = (12,1))]]

    window = sg.Window('Blink Counter', layout, margins=(50,50))
    
    blinksInSession = 0
    totalTime = 0
    while True:
        event, values = window.read()
        if event == 'Track Blinks':
            blinks, time = Eye.startVideo()
            blinksInSession += blinks
            totalTime += time
        if event == 'Blink Graph':
            Eye.plot()
        if event == 'Track & Graph':
            blinks, time = Eye.showBoth()
            blinksInSession += blinks
            totalTime += time
        if event == 'Text Tracker':
            blinks, time = Eye.showStats()
            blinksInSession += blinks
            totalTime += time
        if event == 'Exit' or event == sg.WIN_CLOSED:
            dataFile.write("Average BPM: " + str(format(blinksInSession/totalTime*60, ".1f")) + "\n")
            dataFile.close()
            break
    window.close()




if __name__ == "__main__":
    main()