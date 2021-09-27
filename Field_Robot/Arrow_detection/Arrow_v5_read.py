import cv2
import numpy as np
import matplotlib.pyplot as plt
import math
import time


"""

固定contourArea的orientation或定義評分方式
constants最佳化
反光

"""


path = "C:\\Users\\BERLIN CHEN\\Desktop\\2021FR\\Photos\\red_arrow6.1.jpg"

Hmin_red1 = 0
Smin_red1 = 50
Vmin_red1 = 20
Hmax_red1 = 10
Smax_red1 = 255
Vmax_red1 = 255

Hmin_red2 = 175
Smin_red2 = 50
Vmin_red2 = 20
Hmax_red2 = 180
Smax_red2 = 255
Vmax_red2 = 255

Guassian_ksize = 1

convex_initial_const = 5  # 5
convex_final_const = 10
concave_initial_const = 1  # 5
concave_final_const = 20   # 7,11,12,13

least_area = 10 # adjust by camera
least_arclength = 20 # adjust by camera

criticalArea = 20

tanA = 0.47 # tan25
tanB = 2.14 # tan65

PNdelta_conv = 40
PNdelta_div = 100
# Rdelta/Ldelta: 12/222 218/1 2/216


def cnt_convex_approx(cnt,initial_const,final_const):
    hull = cv2.convexHull(cnt)
    epslion_unit = 0.01*cv2.arcLength(hull,True)
    const = initial_const # low thershold
    approx = []
    while True :
        approx_convex = cv2.approxPolyDP(hull,epslion_unit*const,True)
        if len(approx_convex) == 5 :
            approx = approx_convex
            #print("\nFind convex contour with 5 vertices")
            #print("convex approx const:",const)
            return True,approx_convex
            break
        if const == final_const : # high thershold
            #print("Can't find convex contour, vertices:",len(approx_convex))
            return None,approx_convex
            break
        const += 1
   
def cnt_concave_approx(cnt,initial_const,final_const):
    hull = cv2.convexHull(cnt)
    epslion_unit = 0.001*cv2.arcLength(hull,True)
    const = initial_const # low thershold
    approx = []
    while True :
        approx_concave = cv2.approxPolyDP(cnt,epslion_unit*const,True)
        if len(approx_concave) == 7 :
            approx = approx_concave
            #print("\nFind concave contour with 7 vertices")
            #print("concave approx const:",const)
            return True,approx_concave
            break
        if const == final_const : # high thershold
            #print("Can't find concave contour, vertices:",len(approx_concave))
            return None,approx_concave
            break
        const += 1        
    
    
def convex_concave_Test(cnt,credit):
    if cv2.isContourConvex(cnt) == True:
        #print("the contour is not arrow: convex")
        return False,credit
    else:
        return True,credit

def convexity_defect_Test(cnt,credit):
    try:
        cnt = cv2.approxPolyDP(cnt,0.01*cv2.arcLength(cnt,True),True)
        hull = cv2.convexHull(cnt, returnPoints=False)
        defects = cv2.convexityDefects(cnt, hull)
        #print(defects[0])
        if len(defects[0])!=0:
            #print("defects are found")
            return True,credit
        else:
            return False,credit
    
    except:
        return False,credit
         

def convex_vertices_Test(cnt,credit):
    arrow, approx_convex = cnt_convex_approx(cnt,convex_initial_const,convex_final_const)
    if len(approx_convex) == 5 :
        return True,credit
    else :
        return False,credit

def concave_vertices_Test(img,cnt,credit):
    const = 5 
    arrow, approx_concave = cnt_concave_approx(cnt,concave_initial_const,concave_final_const)
    #print(approx_concave)
    cv2.drawContours(img,[approx_concave],0,(132,100,210),1) # light purple to draw convex approx 
    if len(approx_concave) == 7:
        for point in range(len(approx_concave)):
                x = approx_concave[point][0][0]
                y = approx_concave[point][0][1]
                cv2.circle(img,(x,y),2,(132,100,210),-1)
                text1 = '(' + str(x) + ',' + str(y) + ')'    
        return True,credit,img
    else:
        return False,credit,img
        
        
def x_config_Test(cnt,credit):
    arrow, approx_convex = cnt_convex_approx(cnt,convex_initial_const,convex_final_const)
    if len(approx_convex) != 5:
        return False,credit,'N'
    else:  
        xlist = []
        for point in range(len(approx_convex)):
            x = approx_convex[point][0][0]
            xlist.append(x)
        xlist = sorted(xlist,reverse=True)
        deltaE = xlist[0] - xlist[1]
        deltaE2 = xlist[1] - xlist[2]
        deltaW = xlist[3] - xlist[4]
        deltaW2 = xlist[2] - xlist[3]
        if deltaE > deltaE2 and deltaW < deltaW2 and deltaE > deltaW :
            #print("x_config_Test: Right arrow")
            return True,credit,'R'
        elif deltaE < deltaE2 and deltaW > deltaW2 and deltaE < deltaW :
            #print("x_config_Test: Left Arrow")
            return True,credit,'L'
        else:
            return False,credit,'N'
   
def y_config_Test(cnt,credit):
    arrow, approx_convex = cnt_convex_approx(cnt,convex_initial_const,convex_final_const)
    if len(approx_convex) != 5:
        return False,credit
    else:  
        ylist = []
        for point in range(len(approx_convex)):
            y = approx_convex[point][0][1]
            ylist.append(y)
        ylist = sorted(ylist,reverse=True)
        deltaN = ylist[0] - ylist[1]
        deltaN2 = ylist[1] - ylist[2]
        deltaS = ylist[3] - ylist[4]
        deltaS2 = ylist[2] - ylist[3]
        deltaM = deltaN2 + deltaS2
        if deltaM > deltaN and deltaM > deltaS :
            return True,credit
        else :
            return False,credit
   
   
def M_pos_Test(img,cnt,credit,coef):
    M = cv2.moments(cnt)
    if int(M["m00"]) != 0 :
        Cx = int(M["m10"]/M["m00"])
        Cy = int(M["m01"]/M["m00"])
        cv2.circle(img,(Cx,Cy),4,(110,100,100),-1)
        arrow, approx_convex = cnt_convex_approx(cnt,convex_initial_const,convex_final_const)
        if len(approx_convex) != 5:
            return False,credit,None,coef,img
        else:  
            xlist = []
            ylist = []
            for point in range(len(approx_convex)):
                x = approx_convex[point][0][0]
                y = approx_convex[point][0][1]
                xlist.append(x)
                ylist.append(y)
            x_max = max(xlist)
            x_min = min(xlist)
            y_max = max(ylist)
            y_min = min(ylist)
            d = 2*cv2.arcLength(cnt,True)
            error = math.sqrt(((x_max + x_min)/2)**2 + ((y_max + y_min)/2)**2)
            if error < d :
                #print(error,d)
                return True,credit,None,coef,img
            else :
                #print(error,d)
                return False,credit,None,coef,img
    else:
        return False,credit,None,coef,img
 
def least_area_Test(cnt,credit):
    area = abs(cv2.contourArea(cnt,True))
    thershold = least_area
    if area > thershold :
        #print("area:",area,"thershold:",thershold)
        return True,credit
    else :
        #print("area:",area,"thershold:",thershold)
        return False,credit
        
def least_arclength_Test(cnt,credit):
    length = cv2.arcLength(cnt,True)
    thershold = least_arclength
    if length > thershold :
        #print("length:",length,"thershold:",thershold)
        return True,credit
    else:
        #print("length:",length,"thershold:",thershold)
        return False,credit      
   

def find_range(img,best_cnt):
    arrow, approx_convex = cnt_convex_approx(best_cnt,convex_initial_const,convex_final_const)
    try:
        xlist = []
        ylist = []
        for point in range(len(approx_convex)):
            x = approx_convex[point][0][0]
            y = approx_convex[point][0][1]
            xlist.append(x)
            ylist.append(y)
        xlist = sorted(xlist,reverse=True)
        ylist = sorted(ylist,reverse=True)
        x_range = xlist[0] - xlist[4]
        y_range = ylist[0] - ylist[4]
        #print("x_range:",x_range,"y_range:",y_range)
        cv2.rectangle(img,(xlist[4],ylist[4]),(xlist[0],ylist[0]),(52,200,220),1)
        return img,xlist[4],ylist[4],x_range,y_range
    except:
        return img,0,0,0,0
    
def HoughLinesAnalysis(focus,lines):
    if lines is not None:
        Plist = []
        Nlist = []
        for i in range(0, len(lines)):
            aline = lines[i][0]
            x1 = aline[0]
            x2 = aline[2]
            y1 = aline[1]
            y2 = aline[3]
            
            # cv2.circle(focus,(x1,y1),6,(132,100,210),-1)  # start point
            # cv2.circle(focus,(x2,y2),6,(172,100,210),-1)  # end point
            
            if x1 != x2 :
                m = -1*(y2-y1)/(x2-x1)
            else :
                m = 1000
               
            if m > -1*tanA and m < tanA :
                #print("Find H line")
                cv2.putText(focus, 'H', ((x1+x2)//2, y1+5), cv2.FONT_HERSHEY_PLAIN, 2, (20,100,240), 1, cv2.LINE_AA)
                cv2.line(focus, (x1, y1), (x2, y2), (20,100,200), 3, cv2.LINE_AA)
            elif m > tanB or m < -1*tanB :
                #print("Find V line")
                cv2.putText(focus, 'V', (x1-20, (y1+y2)//2), cv2.FONT_HERSHEY_PLAIN, 2, (5,100,240), 1, cv2.LINE_AA)
                cv2.line(focus, (x1, y1), (x2, y2), (5,100,200), 3, cv2.LINE_AA)
            elif m > tanA and m < tanB :
                #print("Find P line, m=",m)
                cv2.putText(focus, 'P', (x2, (y1+y2)//2), cv2.FONT_HERSHEY_PLAIN, 2, (90,100,240), 1, cv2.LINE_AA)
                cv2.line(focus, (x1, y1), (x2, y2), (90,100,200), 3, cv2.LINE_AA)
                startPoint = tuple((x1,y1))
                endPoint = tuple((x2,y2))
                Plist.append(startPoint)
                Plist.append(endPoint)
                #print("Plist append:",startPoint,',',endPoint)
                
            elif m < -1*tanA and m > -1*tanB :
                #print("Find N line, m=",m)
                cv2.putText(focus, 'N', (x2-20, (y1+y2)//2), cv2.FONT_HERSHEY_PLAIN, 2, (70,100,240), 1, cv2.LINE_AA)
                cv2.line(focus, (x1, y1), (x2, y2), (70,100,200), 3, cv2.LINE_AA)
                startPoint = tuple((x1,y1))
                endPoint = tuple((x2,y2))
                Nlist.append(startPoint)
                Nlist.append(endPoint)
                #print("Nlist append:",startPoint,',',endPoint)
            
            # if i == 0:
                # cv2.line(focus, (x1, y1), (x2, y2), (20,100,200), 10, cv2.LINE_AA)
            # if i == 1:
                # cv2.line(focus, (x1, y1), (x2, y2), (30,100,200), 10, cv2.LINE_AA)
            # if i == 2:
                # cv2.line(focus, (x1, y1), (x2, y2), (40,100,200), 10, cv2.LINE_AA)
            # if i == 3:
                # cv2.line(focus, (x1, y1), (x2, y2), (50,100,200), 10, cv2.LINE_AA)
            # if i == 4:
                # cv2.line(focus, (x1, y1), (x2, y2), (60,100,200), 10, cv2.LINE_AA)
            # if i == 5:
                # cv2.line(focus, (x1, y1), (x2, y2), (80,100,200), 10, cv2.LINE_AA)
            # if i == 6:
                # cv2.line(focus, (x1, y1), (x2, y2), (100,100,200), 10, cv2.LINE_AA)
            # if i == 7:
                # cv2.line(focus, (x1, y1), (x2, y2), (120,100,200), 10, cv2.LINE_AA)
            # if i == 8:
                # cv2.line(focus, (x1, y1), (x2, y2), (140,100,200), 10, cv2.LINE_AA)
            # if i == 9:
                # cv2.line(focus, (x1, y1), (x2, y2), (160,100,200), 10, cv2.LINE_AA)
            # if i == 10:
                # cv2.line(focus, (x1, y1), (x2, y2), (175,100,200), 10, cv2.LINE_AA)
        if Plist != [] and Nlist != [] :
            sortedP = sorted(Plist, key = lambda P : P[0],reverse=True)
            sortedN = sorted(Nlist, key = lambda N : N[0],reverse=True)
            #print("sorted Plist:",sortedP)
            #print("sorted Nlist:",sortedN)
            
            Plist_maxx_y = sortedP[0][1]
            Plist_minx_y = sortedP[len(sortedP)-1][1]
            Nlist_maxx_y = sortedN[0][1]
            Nlist_minx_y = sortedN[len(sortedN)-1][1]
            cv2.circle(focus,(sortedN[0][0],Nlist_maxx_y),10,(132,100,210),-1)  # right point
            cv2.circle(focus,(sortedP[0][0],Plist_maxx_y),10,(132,100,210),-1)  # right point
            
            cv2.circle(focus,(sortedN[len(sortedN)-1][0],Nlist_minx_y),10,(172,100,210),-1)  # left point
            cv2.circle(focus,(sortedP[len(sortedP)-1][0],Plist_minx_y),10,(172,100,210),-1)  # left point
          
            Rdelta = abs(Plist_maxx_y - Nlist_maxx_y)
            Ldelta = abs(Plist_minx_y - Nlist_minx_y)
            #print("Rdelta",Rdelta,"Ldelta",Ldelta)
            cv2.putText(focus, "HoughLines", (310,280), cv2.FONT_HERSHEY_PLAIN, 2, (30,100,255), 2, cv2.LINE_AA) 
            if Rdelta < PNdelta_conv and Ldelta > PNdelta_div :
                #print("HoughLines transform Test: Right Arrow")
                cv2.putText(focus, "result: R", (40,280), cv2.FONT_HERSHEY_PLAIN, 2, (5,100,255), 2, cv2.LINE_AA) 
                return focus,'R'
            elif Rdelta > PNdelta_div and Ldelta < PNdelta_conv :
                #print("HoughLines transform Test: Left Arrow")
                cv2.putText(focus, "result: L", (20,280), cv2.FONT_HERSHEY_PLAIN, 2, (5,100,255), 2, cv2.LINE_AA) 
                return focus,'L'
            else :
                cv2.putText(focus, "no result", (20,280), cv2.FONT_HERSHEY_PLAIN, 2, (5,100,255), 2, cv2.LINE_AA) 
                return focus,'N'
        else:
            #print("Can't find N/P line")
            print("HoughLines transform Test: None")
            return focus,'N'
    else:
        print("HoughLines transform Test: None")
        return focus,'N'
        
def find_arrow(frame):
    try:
        orig = frame
        orig = cv2.resize(orig, (800, 450)) # 16:9
        #cv2.imshow("original",orig)

        """ cropping """
        x = 150
        y = 100
        w = 500
        h = 300
        cropped = orig[y:y+h, x:x+w]
        #cv2.imshow("cropped",cropped)

        """ thresholding """
        cvted_img = cv2.cvtColor(cropped, cv2.COLOR_BGR2RGB)
        cvted_img = cv2.cvtColor(cvted_img, cv2.COLOR_RGB2HSV)

        lower_red1 = np.array([Hmin_red1, Smin_red1, Vmin_red1])
        upper_red1 = np.array([Hmax_red1, Smax_red1, Vmax_red1])
        mask_red1 = cv2.inRange(cvted_img, lower_red1, upper_red1)
        #cv2.imshow("red1 mask", mask_red1)
        lower_red2 = np.array([Hmin_red2, Smin_red2, Vmin_red2])
        upper_red2 = np.array([Hmax_red2, Smax_red2, Vmax_red2])
        mask_red2 = cv2.inRange(cvted_img, lower_red2, upper_red2)
        #cv2.imshow("red2 mask", mask_red2)

        mask_red = cv2.bitwise_or(mask_red1,mask_red2)
        #cv2.imshow("mask_red", mask_red)

        """ morphology """
        img = mask_red
        kernel = np.ones((4,4),np.uint8)
        #erosion = cv2.erode(img,kernel,iterations = 1)
        dilation = cv2.dilate(img,kernel,iterations = 1)
        #opening = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
        closing = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
        showMorphology = cv2.hconcat([dilation,closing])
        #cv2.imshow("Morphology",showMorphology)

        """ edge, Canny """
        canny = cv2.Canny(closing, 60, 100)
        #cv2.imshow("Canny",canny)

        """ show Process """
        cvted_img = cv2.cvtColor(cvted_img,cv2.COLOR_HSV2BGR)
        mask_red = cv2.cvtColor(mask_red,cv2.COLOR_GRAY2BGR)
        mask_red = cv2.cvtColor(mask_red,cv2.COLOR_BGR2HSV)
        cv2.putText(mask_red, "Red mask", (320,280), cv2.FONT_HERSHEY_PLAIN, 2, (30,100,255), 2, cv2.LINE_AA)
        mask_red = cv2.cvtColor(mask_red,cv2.COLOR_HSV2BGR)
        closing = cv2.cvtColor(closing,cv2.COLOR_GRAY2BGR)
        closing1 = cv2.cvtColor(closing,cv2.COLOR_BGR2HSV)
        cv2.putText(closing1, "Morphology", (290,280), cv2.FONT_HERSHEY_PLAIN, 2, (30,100,255), 2, cv2.LINE_AA)
        closing1 = cv2.cvtColor(closing1,cv2.COLOR_HSV2BGR)

        cannyBGR = cv2.cvtColor(canny,cv2.COLOR_GRAY2BGR)
        cannyBGR = cv2.cvtColor(cannyBGR,cv2.COLOR_BGR2HSV)
        cv2.putText(cannyBGR, "Canny", (380,280), cv2.FONT_HERSHEY_PLAIN, 2, (30,100,255), 2, cv2.LINE_AA)
        cannyBGR = cv2.cvtColor(cannyBGR,cv2.COLOR_HSV2BGR)

        cropped_mask = cv2.hconcat([cvted_img,mask_red])
        morphol_canny = cv2.hconcat([closing1,cannyBGR])
        DisplayProcess = cv2.vconcat([cropped_mask,morphol_canny])
        # cv2.imshow("Process",DisplayProcess)

        """ find contours, search for the arrow shape one """
        cvted_img = cv2.cvtColor(cvted_img,cv2.COLOR_BGR2HSV)
        contoursImage = cvted_img.copy()
        #print(contoursImage.shape[1])
        contours, hierarchy = cv2.findContours(canny, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        if contours:   
            cnt_map = sorted(contours,key=cv2.contourArea,reverse=True)
            #print("There are",len(cnt_map),"contours:\n")
            count = 0
            record = 0
            index = 0
            scoreList = []
            best_cnt = cnt_map[0]
            for cnt in cnt_map:
                #print("\n\nContour",count,":")
                ifArrow1, credit1  = convex_concave_Test(cnt,3)
                ifArrow2, credit2  = convexity_defect_Test(cnt,2)
                
                ifArrow3, credit3 = convex_vertices_Test(cnt,6)
                ifArrow4, credit4, contoursImage = concave_vertices_Test(contoursImage,cnt,2)
                
                ifArrow5, credit5, xconfigDir  = x_config_Test(cnt,3)
                ifArrow6, credit6  = y_config_Test(cnt,2)
                
                ifArrow7, credit7  = least_area_Test(cnt,10)
                ifArrow8, credit8 = least_arclength_Test(cnt,4)
                
                ifArrowList = [ifArrow1,ifArrow2,ifArrow3,ifArrow4,ifArrow5,ifArrow6,ifArrow7,ifArrow8]
                creditList = [credit1,credit2,credit3,credit4,credit5,credit6,credit7,credit8]

                
                """ Calculate the score """
                score = 0
                for i in range(len(ifArrowList)):
                    if ifArrowList[i] == True :
                        score += 1*creditList[i]
                
                """ Bonus by heuristics """
                if count <= 5:
                    score += 4 # front contours -> larger area
                    
                if score == record and count < 4:
                    score += 5 # almost the same bonus
                
                """ Best-matched contour """
                #print("score:",score,'\n')         
                if score > record:
                    record = score
                    best_cnt = cnt
                    index = count
                    
                if score > 15 :   # Well-matched contours: noted in light blue
                    arrow, approx_convex = cnt_convex_approx(cnt,convex_initial_const,convex_final_const)
                    cv2.drawContours(contoursImage,[approx_convex],0,(90,100,210),2) # light blue to draw convex approx
                    cv2.putText(contoursImage, str(score), (approx_convex[0][0][0],approx_convex[0][0][1]-10), cv2.FONT_HERSHEY_PLAIN, 2, (90,100,210), 2, cv2.LINE_AA)
                elif score > 10 :   # little-matched contours: noted in light green
                    arrow, approx_convex = cnt_convex_approx(cnt,convex_initial_const,convex_final_const)
                    cv2.drawContours(contoursImage,[approx_convex],0,(60,100,210),1) # light green to draw convex approx 
                    cv2.putText(contoursImage, str(score), (approx_convex[0][0][0],approx_convex[0][0][1]-10), cv2.FONT_HERSHEY_PLAIN, 1, (60,100,210), 1, cv2.LINE_AA)
            
                scoreList.append(score)            
                count += 1
            
            """ Conclusion for all contours """
            #print("\n\n\n--------------------------------------------------------------\n\n\n")
            scoreList = sorted(scoreList,reverse=True)
            #print("Candidates:",count,"contours\nScore list:",scoreList)
            #print(best_cnt,record,index)
            
            """ For the most probable contour """
            #print("Best score:",record)
            #print("Index:",index)
            
            arrow, best_approx = cnt_convex_approx(best_cnt,convex_initial_const,concave_final_const)
            if cv2.contourArea(best_approx) > least_area:
                findArrow = True
            else:
                findArrow = False
                
            if record >= 40:
                probstr = "'definitely'"
            elif record >= 35:
                probstr = "'probablely'"
            elif record >= 30:
                probstr = "'likely to'"
            else:
                probstr = "'perhaps'"

            #print("Score:",record)
            # if findArrow == True:      
                # print("\nThe arrow is",probstr,"be found\n")
            # if findArrow == False: 
                # print("\nThe arrow can't be found")
            
            """ All tests result for the most probable contour """ 
            testResultImage = canny.copy()
            ifArrow1, credit1  = convex_concave_Test(cnt,3)
            ifArrow2, credit2  = convexity_defect_Test(cnt,2)
            
            ifArrow3, credit3 = convex_vertices_Test(cnt,6)
            ifArrow4, credit4, testResultImage = concave_vertices_Test(testResultImage,cnt,2)
            
            ifArrow5, credit5, xconfigDir  = x_config_Test(cnt,3)
            ifArrow6, credit6  = y_config_Test(cnt,2)
            
            ifArrow7, credit7  = least_area_Test(cnt,10)
            ifArrow8, credit8 = least_arclength_Test(cnt,4)
            
            print("\nconvex_concave_Test:",ifArrow1)
            print("convexity_defect_Test",ifArrow2)
            print("convex_vertices_Test:",ifArrow3)
            print("concave_vertices_Test:",ifArrow4)
            print("x_config_Test:",ifArrow5,"Direction:",xconfigDir)
            print("y_config_Test:",ifArrow6)
            print("least_area_Test:",ifArrow7)
            print("least_arclength_Test:",ifArrow8)
            
            """ Convex approx, show points on convexImage"""
            arrowcheck1, approx_convex = cnt_convex_approx(best_cnt,convex_initial_const,convex_final_const)
            #print("\nArrow convex check:",arrowcheck1)
            #print(approx_convex)
            
            convexImage = canny.copy()
            convexImage = cv2.cvtColor(convexImage,cv2.COLOR_GRAY2BGR)
            convexImage = cv2.cvtColor(convexImage,cv2.COLOR_BGR2HSV)
            cv2.drawContours(convexImage,[approx_convex],0,(30,100,210),2) # light yellow to draw convex approx 
            areaText = "Area:"+str(cv2.contourArea(best_cnt))   #+"  countNonZero:"+str(cv2.countNonZero(cropped))
            #print(areaText)
            cv2.putText(convexImage, areaText, (approx_convex[0][0][0]-180,approx_convex[0][0][1]-10), cv2.FONT_HERSHEY_PLAIN, 3, (30,100,210), 4, cv2.LINE_AA)
            for point in range(len(approx_convex)):
                    x = approx_convex[point][0][0]
                    y = approx_convex[point][0][1]
                    cv2.circle(convexImage,(x,y),4,(30,100,210),-1)
                    text1 = '(' + str(x) + ',' + str(y) + ')'
                    cv2.putText(convexImage, text1, (x-15, y-5), cv2.FONT_HERSHEY_PLAIN, 0.8, (30,100,210), 1, cv2.LINE_AA)
            
            
            """ show the best convex contour on contoursImage """
            text2 = str(record)
            cv2.putText(contoursImage, text2, (approx_convex[0][0][0]+20,approx_convex[0][0][1]-10), cv2.FONT_HERSHEY_PLAIN, 3, (30,100,210), 4, cv2.LINE_AA)
            cv2.drawContours(contoursImage,[approx_convex],0,(30,100,210),2)
            
            
            """ Concave approx, show points on concaveImage"""
            arrowcheck2, approx_concave = cnt_concave_approx(best_cnt,concave_initial_const,concave_final_const)
            #print("\nArrow concave check:",arrowcheck2)
            #print(approx_concave)
            
            concaveImage = canny.copy()
            concaveImage = cv2.cvtColor(concaveImage,cv2.COLOR_GRAY2BGR)
            concaveImage = cv2.cvtColor(concaveImage,cv2.COLOR_BGR2HSV)
            cv2.drawContours(concaveImage,[approx_concave],0,(132,100,210),2) # light purple to draw concave approx   
            
            if len(approx_concave) == 7 :
                #print("concave points:",len(approx_concave))
                for point in range(len(approx_concave)):
                        x = approx_concave[point][0][0]
                        y = approx_concave[point][0][1]
                        cv2.circle(concaveImage,(x,y),4,(132,100,210),-1)
                        text3 = '(' + str(x) + ',' + str(y) + ')'
                        cv2.putText(concaveImage, text3, (x-15, y-5), cv2.FONT_HERSHEY_PLAIN, 0.8, (132,100,240), 1, cv2.LINE_AA)
            
            
            """ further cropping accd. to arrow size """
            furthercrop = canny.copy()
            furthercrop = cv2.cvtColor(furthercrop,cv2.COLOR_GRAY2BGR)
            furthercrop = cv2.cvtColor(furthercrop,cv2.COLOR_BGR2HSV)
            houghImage = furthercrop.copy()
            furthercrop, x_min, y_min, x_range, y_range = find_range(furthercrop,best_cnt)
            if x_range != 0 and y_range != 0 :
                y_start = int(y_min - 0.2* y_range)
                x_start = int(x_min - ((1.4* y_range* 5/3)-x_range)/2)
                houghImage = houghImage[y_start:y_start+int(1.4*y_range), x_start:x_start+int(1.4* y_range* 5/3)]
                try:
                    houghImage = cv2.resize(houghImage, (500, 300))
                except:
                    print(houghImage.shape)
                furthercrop = furthercrop[y_start:y_start+int(1.4*y_range), x_start:x_start+int(1.4* y_range* 5/3)]
                furthercrop = cv2.resize(furthercrop, (500, 300))
                
            """ HoughLines transform after further cropping """   
            houghImage = cv2.cvtColor(houghImage, cv2.COLOR_HSV2BGR)
            houghImage = cv2.cvtColor(houghImage, cv2.COLOR_BGR2GRAY)
            lines = cv2.HoughLinesP(houghImage,rho=1,theta=1*np.pi/180,threshold=30,lines=None, minLineLength=40, maxLineGap=5)
            houghImage = cv2.cvtColor(houghImage, cv2.COLOR_GRAY2BGR)
            houghImage = cv2.cvtColor(houghImage, cv2.COLOR_BGR2HSV)
            
            houghImage,HoughLinesDir = HoughLinesAnalysis(houghImage,lines)
            
            houghImage = cv2.cvtColor(houghImage, cv2.COLOR_HSV2BGR)
            #cv2.imshow("HoughLines",houghImage)
                
            """ Determine the arrow direction """
           
            #print("\nx config Test:",xconfigDir)
            #print("\nHoughLines transform Test:",HoughLinesDir)
            if xconfigDir == 'R' and HoughLinesDir == 'R':
                #print("\nArrow Direction: 'definitely' Right")
                cv2.putText(furthercrop, "'definitely' Right", (120,40), cv2.FONT_HERSHEY_PLAIN, 2, (52,200,220), 2, cv2.LINE_AA)
            if xconfigDir == 'L' and HoughLinesDir == 'L' :
                #print("\nArrow Direction: 'definitely' Left")
                cv2.putText(furthercrop, "'definitely' Left", (120,40), cv2.FONT_HERSHEY_PLAIN, 2, (52,200,220), 2, cv2.LINE_AA)        
            
            if (xconfigDir == 'R' and HoughLinesDir == 'N') or (xconfigDir == 'N' and HoughLinesDir == 'R') :
                #print("\nArrow Direction: 'probably' Right")
                cv2.putText(furthercrop, "'probably' Right", (120,40), cv2.FONT_HERSHEY_PLAIN, 2, (52,200,220), 2, cv2.LINE_AA) 
            if (xconfigDir == 'L' and HoughLinesDir == 'N') or (xconfigDir == 'N' and HoughLinesDir == 'L') :
                #print("\nArrow Direction: 'probably' Left")
                cv2.putText(furthercrop, "'probably' Left", (120,40), cv2.FONT_HERSHEY_PLAIN, 2, (52,200,220), 2, cv2.LINE_AA) 
                
            """ Display Result """
            cv2.putText(contoursImage, "Contours", (330,280), cv2.FONT_HERSHEY_PLAIN, 2, (30,100,255), 2, cv2.LINE_AA)
            contoursImage = cv2.cvtColor(contoursImage,cv2.COLOR_HSV2BGR)
            #cv2.imshow("contoursImage",contoursImage) 
            
            cv2.putText(convexImage, "Convex", (350,280), cv2.FONT_HERSHEY_PLAIN, 2, (30,100,255), 2, cv2.LINE_AA)
            if xconfigDir == 'R' :
                cv2.putText(convexImage, "result: R", (20,280), cv2.FONT_HERSHEY_PLAIN, 2, (5,100,255), 2, cv2.LINE_AA)  
            if xconfigDir == 'L' :
                cv2.putText(convexImage, "result: L", (20,280), cv2.FONT_HERSHEY_PLAIN, 2, (5,100,255), 2, cv2.LINE_AA)   
            else :
                cv2.putText(convexImage, "no result", (20,280), cv2.FONT_HERSHEY_PLAIN, 2, (5,100,255), 2, cv2.LINE_AA)     
            convexImage = cv2.cvtColor(convexImage,cv2.COLOR_HSV2BGR)
            #cv2.imshow("convexImage",convexImage)  
            
            cv2.putText(concaveImage, "Concave", (340,280), cv2.FONT_HERSHEY_PLAIN, 2, (30,100,255), 2, cv2.LINE_AA)    
            concaveImage = cv2.cvtColor(concaveImage,cv2.COLOR_HSV2BGR)
            #cv2.imshow("concaveImage",concaveImage)  
            
            cv2.putText(furthercrop, "Furthercrop", (280,280), cv2.FONT_HERSHEY_PLAIN, 2, (30,100,255), 2, cv2.LINE_AA) 
            furthercrop = cv2.cvtColor(furthercrop,cv2.COLOR_HSV2BGR)
            #cv2.imshow("furthercrop",furthercrop)
            
            Contour_Concave = cv2.hconcat([contoursImage,concaveImage])
            Convex_Furthercrop = cv2.hconcat([convexImage,furthercrop])
            DisplayPrimaryResult = cv2.vconcat([Contour_Concave, Convex_Furthercrop])
            #cv2.imshow("Primary Result",DisplayPrimaryResult)
            
            Displaytwo = cv2.vconcat([DisplayProcess, DisplayPrimaryResult])
            Displaytwo = cv2.resize(Displaytwo,(500,600))
            #cv2.imshow("Arrow Detection",Displaytwo)
            
            DisplayFinalResult1 = cv2.hconcat([contoursImage,convexImage])
            DisplayFinalResult2 = cv2.hconcat([houghImage,furthercrop])
            DisplayFinalResult = cv2.vconcat([DisplayFinalResult1, DisplayFinalResult2])
            cv2.imshow("DisplayFinalResult",DisplayFinalResult)
            
            if (xconfigDir == 'R' and HoughLinesDir == 'R') or (xconfigDir == 'R' and HoughLinesDir == 'N') or (xconfigDir == 'N' and HoughLinesDir == 'R'):
                return int(cv2.contourArea(best_cnt)) , 'R'
            elif (xconfigDir == 'L' and HoughLinesDir == 'L') or (xconfigDir == 'L' and HoughLinesDir == 'L') or (xconfigDir == 'N' and HoughLinesDir == 'L'):
                return int(cv2.contourArea(best_cnt)) , 'L'
            else:
                return int(cv2.contourArea(best_cnt)) , 'N'

        else:
            print("No contours")
            return 0,'N'
        
    except:
        print("Exception: find arrow error")
        return 0,'N'
                
                
# try:
camera_port = 1
cap = cv2.VideoCapture(cv2.CAP_DSHOW + camera_port) # cap = cv2.VideoCapture(cv2.CAP_DSHOW + camera_port)
cap.set(cv2.CAP_PROP_EXPOSURE,-2)
print("Start capturing video from the camera")

if cap.isOpened() == False:
    print("Error: Failed to read the video stream")
else:
    print("Read images successfully\n")

countImage = 0
while cap.isOpened():  # Capture frame-by-frame
    ret, frame = cap.read()
    if countImage == 0:
        print("height:",frame.shape[0],"width:",frame.shape[1],"channel:",frame.shape[2])
        print("Image type:",type(frame))
        
    #print("\ncount:",countImage,'\n')
    cv2.imshow("original",frame)
    if ret == True:
        Area, Dir = find_arrow(frame)
        print("\nArea:",Area,"\nDir:",Dir,'\n')
        
        if cv2.waitKey(25) & 0xFF == ord("q"):
            break
        countImage += 1
        time.sleep(0.1)
    else:
        print("Error: no ret")
        break
    
cap.release()
cv2.destroyAllWindows()
        
# except :
    # print("Error: Failed to capture the video")
