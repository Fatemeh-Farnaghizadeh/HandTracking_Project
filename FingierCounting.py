import mediapipe as mp
import cv2
import HandTracking_Module as htm

detector = htm.HandTracking(static_image_mode=True, max_num_hands=2)
cap = cv2.VideoCapture('1.mp4')
WCap = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
HCap = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
cap.set(3, WCap)
cap.set(4, HCap)

output_path = 'output/output_video.mp4'
fourcc = cv2.VideoWriter_fourcc(*'mp4v') 
fps = cap.get(cv2.CAP_PROP_FPS)
frame_width, frame_height = WCap, HCap  
video_writer = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))

# LM number of fingertips
points = [4, 8, 12, 16, 20]

while True:
    ret, frame = cap.read()

    if ret:
        upFingers = []
        sides = []
        frame = detector.findHands(frame)
        Hand1, side = detector.findPosition(frame, hand_num=0, draw=False)
        
        if len(Hand1) != 0:
            
            if side == 'right':

                if Hand1[4][1] > Hand1[3][1]:
                    upFingers.append(1)
            
                else:
                    upFingers.append(0)
            else: 
                
                if Hand1[4][1] < Hand1[3][1]:
                    upFingers.append(1)
            
                else:
                    upFingers.append(0)
            
            for tip in points[1:]:

                if Hand1[tip][2] < Hand1[tip-2][2]:
                    upFingers.append(1)

                else:
                        upFingers.append(0)
            
            hand1Val = upFingers.count(1)
            cv2.putText(frame, side + f'= {hand1Val}', (25, 100), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)

        Hand2, side = detector.findPosition(frame, hand_num=1, draw=False)
        sides.append(side)

        if len(Hand2) != 0:

            if side == 'right':

                if Hand2[4][1] > Hand2[3][1]:
                    upFingers.append(1)
            
                else:
                    upFingers.append(0)

            else: 
                
                if Hand2[4][1] < Hand2[3][1]:
                    upFingers.append(1)
            
                else:
                    upFingers.append(0)
          
            for tip in points[1:]:

                if Hand2[tip][2] < Hand2[tip-2][2]:
                    upFingers.append(1)

                else:
                    upFingers.append(0)

            hand2Val = upFingers[5:].count(1)
            cv2.putText(frame, side + f'= {hand2Val}', (25, 150), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)

        if len(Hand1) != 0:
            total = upFingers.count(1)           
            cv2.putText(frame, f'total = {total}', (25, 200), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 2)

        video_writer.write(frame)

        cv2.imshow('image', frame)
        
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break
