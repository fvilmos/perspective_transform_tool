import cv2
import numpy as np
from .imagewarp import ImageWarp

class KeyMouseHandler():
    hud_info = ''
    dict_list = dict()
    global_state = 0
    global_state_locked = 0
    iw_obj = ImageWarp()
    pts =[]
    def __init__(self,in_img_size=(320,240), out_img_size=(320,240)):
        # HUD font values
        self.sizef = 0.3
        self.typef = cv2.FONT_HERSHEY_SIMPLEX
        self.color = [0,255,0]
        self.sizeb = 1

        self.dict_list = dict()
        self.in_img_size = in_img_size
        self.out_img_size = out_img_size
        #self.global_state = 0

        
        self.key_list = [
        {'key':'o','fn':'fn_select_in_points', 'state':1,'color':[0,0,255],'trans':1,'nr_points':4,'info':'select with mouse 4 input points, adjust with wasd'},
        {'key':'p','fn':'fn_select_out_points', 'state':2,'color':[255,0,0],'trans':2,'nr_points':4,'info':'select with mouse 4 output points, ajust with wasd'},
        {'key':'t','fn':'fn_transform', 'state':3,'info':'transform'},
        {'key':'e','fn':'fn_edit_np', 'state':4,'color':[255,0,255],'nr_points':1,'info':'edit the nearest point'},
        ]

        cv2.namedWindow('Test_detections')
        cv2.setMouseCallback('Test_detections',self.get_mouse)

    def fn_edit_np(self,k_it):
        # lock state
        if KeyMouseHandler.global_state == k_it['state']:
            # lock state
            KeyMouseHandler.global_state_locked = 1

            if len(KeyMouseHandler.pts)>0:
                # get the reference point
                pt = KeyMouseHandler.pts[-1]
                KeyMouseHandler.pts = []

                # get all list with reference points
                # comput the minimal distance, than update the point
                min_dist=KeyMouseHandler.iw_obj.img_w

                for it in self.key_list:
                    if it['fn'] in KeyMouseHandler.dict_list:
                        ll_val = KeyMouseHandler.dict_list[it['fn']]
                        for v in ll_val:
                            # compute euclidina distance
                            td = np.linalg.norm(np.array(pt)-np.array(v))
                            if td < min_dist:
                                min_dist = td


                # update point
                for it in self.key_list:
                    if it['fn'] in KeyMouseHandler.dict_list:
                        ll_val = KeyMouseHandler.dict_list[it['fn']]
                        for i,v in enumerate(ll_val):
                            # compute euclidina distance
                            td = np.linalg.norm(np.array(pt)-np.array(v))
                            if td == min_dist:
                                ll_val[i] = pt
                
                KeyMouseHandler.global_state_locked = 0
                KeyMouseHandler.global_state = 0
                KeyMouseHandler.hud_info = 'editing mode'

                            
    def fn_transform(self,k_it):
        # get current state
        # make transform
        for it in self.key_list:
            if 'trans' in it:
                if it['trans'] == 1:
                    # we have the input target
                    if it['fn'] in KeyMouseHandler.dict_list:
                        val = KeyMouseHandler.dict_list[it['fn']]
                        # check len
                        if len(val) == it['nr_points']:
                            # change order 1->2->3-4, 1->2->4->3
                            tval = val.copy()
                            tval[2] = val[3]
                            tval[3] = val[2]
                            KeyMouseHandler.iw_obj.set_param(tval,param_index=0)
                if it['trans'] == 2:
                    # we have the output target
                    if it['fn'] in KeyMouseHandler.dict_list:
                        val = KeyMouseHandler.dict_list[it['fn']]
                        # check len
                        if len(val) == it['nr_points']:
                            # change order 1->2->3-4, 1->2->4->3
                            tval = val.copy()
                            tval[2] = val[3]
                            tval[3] = val[2]
                            KeyMouseHandler.iw_obj.set_param(tval,param_index=1)
        self.set_hud_info(k_it['info'])
        
    def fn_inc_y_pts(self,k_it):
        # get current state
        if KeyMouseHandler.global_state != 0:
            for it in self.key_list:
                if it['state'] == KeyMouseHandler.global_state:
                    # get item from list to modify
                    if it['fn'] in KeyMouseHandler.dict_list:
                        ll = KeyMouseHandler.dict_list[it['fn']]
                        val = ll[-1]
                        val[0] +=1
                        ll[-1] = val
                        KeyMouseHandler.dict_list[it['fn']] = ll

        
    def fn_dec_y_pts(self,k_it):
        # get current state
        if KeyMouseHandler.global_state != 0:
            for it in self.key_list:
                if it['state'] == KeyMouseHandler.global_state:
                    # get item from list to modify
                    if it['fn'] in KeyMouseHandler.dict_list:
                        ll = KeyMouseHandler.dict_list[it['fn']]
                        val = ll[-1]
                        val[0] -=1
                        ll[-1] = val
                        KeyMouseHandler.dict_list[it['fn']] = ll

    def fn_dec_x_pts(self,k_it):
        print ('fn_dec_x_pts')
        if KeyMouseHandler.global_state != 0:
            for it in self.key_list:
                if it['state'] == KeyMouseHandler.global_state:
                    # get item from list to modify
                    if it['fn'] in KeyMouseHandler.dict_list:
                        ll = KeyMouseHandler.dict_list[it['fn']]
                        val = ll[-1]
                        val[1] +=1
                        ll[-1] = val
                        KeyMouseHandler.dict_list[it['fn']] = ll

    def fn_inc_x_pts(self,k_it):
        if KeyMouseHandler.global_state != 0:
            for it in self.key_list:
                if it['state'] == KeyMouseHandler.global_state:
                    # get item from list to modify
                    if it['fn'] in KeyMouseHandler.dict_list:
                        ll = KeyMouseHandler.dict_list[it['fn']]
                        val = ll[-1]
                        val[1] -=1
                        ll[-1] = val
                        KeyMouseHandler.dict_list[it['fn']] = ll

    def set_hud_info(self, info):
        KeyMouseHandler.hud_info = info
    
    def fn_select_in_points(self,k_it):
        
        if KeyMouseHandler.global_state == k_it['state']:
            # lock state
            KeyMouseHandler.global_state_locked = 1
            

            if len(KeyMouseHandler.pts)>0:
                # get the point
                pt = KeyMouseHandler.pts[-1]
                KeyMouseHandler.pts = []

                #check if item exists
                ll = []
                if k_it['fn'] in KeyMouseHandler.dict_list:
                    ll = KeyMouseHandler.dict_list[k_it['fn']]
                    ll.append(pt)
                    KeyMouseHandler.dict_list[k_it['fn']] = ll
                else:
                    ll.append(pt)
                    KeyMouseHandler.dict_list[k_it['fn']]=ll
                
                if len(KeyMouseHandler.dict_list[k_it['fn']]) == k_it['nr_points']:
                    self.set_hud_info ("done!!!")
                    KeyMouseHandler.global_state = 0
                    KeyMouseHandler.global_state_locked = 0


            # do stuff
            self.set_hud_info(str(k_it['info']))

    def fn_select_out_points(self,k_it):

        if KeyMouseHandler.global_state == k_it['state']:
            # lock state
            KeyMouseHandler.global_state_locked = 1

            if len(KeyMouseHandler.pts)>0:
                # get the point
                pt = KeyMouseHandler.pts[-1]
                KeyMouseHandler.pts = []

                #check if item exists
                ll = []
                if k_it['fn'] in KeyMouseHandler.dict_list:
                    ll = KeyMouseHandler.dict_list[k_it['fn']]
                    ll.append(pt)
                    KeyMouseHandler.dict_list[k_it['fn']] = ll
                else:
                    ll.append(pt)
                    KeyMouseHandler.dict_list[k_it['fn']]=ll
                
                if len(KeyMouseHandler.dict_list[k_it['fn']]) == k_it['nr_points']:
                    self.set_hud_info ("done!!!")
                    KeyMouseHandler.global_state = 0
                    KeyMouseHandler.global_state_locked = 0


            # do stuff
            self.set_hud_info(str(k_it['info']))

    #===========================
    # cyclic function
    #===========================
    def run (self, key,in_img):
        l_img = in_img.copy()
        for it in self.key_list:
            if ord(it['key']) == key:
                # call the local function attached to the key
                if KeyMouseHandler.global_state_locked == 0:
                    if it['fn'] in KeyMouseHandler.dict_list:
                        KeyMouseHandler.dict_list[it['fn']] = []
                    KeyMouseHandler.global_state = it['state']


            if it['fn'] in KeyMouseHandler.dict_list:
                ll = KeyMouseHandler.dict_list[it['fn']]
                cv2.polylines(in_img,np.array([ll]),isClosed=True,color=[0,255,0])
                for p in ll:
                    cv2.circle(in_img,(p[0],p[1]),3,it['color'],-1)
                    cv2.putText(in_img,str(p),(p[0]+5,p[1]-5),cv2.FONT_HERSHEY_PLAIN,0.6,[0,255,0],1)

            if KeyMouseHandler.global_state == it['state']:
                # call the local function attached to the key
                getattr(globals()['KeyMouseHandler'](),it['fn'])(it)


        cv2.putText(in_img,str(self.hud_info),(int(10),int(14)),cv2.FONT_HERSHEY_PLAIN,0.9,[0,255,0],1)
        ishape = in_img.shape
        KeyMouseHandler.iw_obj.img_w =ishape[1]
        KeyMouseHandler.iw_obj.img_h =ishape[0]
        wimg = KeyMouseHandler.iw_obj.img_warp(l_img)

        KeyMouseHandler.pts = []
        
        return wimg

    def get_mouse(self,event,x,y,flags,param):
        if event == cv2.EVENT_LBUTTONDBLCLK:
            KeyMouseHandler.pts.append([x,y])