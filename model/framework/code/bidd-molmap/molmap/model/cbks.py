from sklearn.metrics import roc_auc_score, precision_recall_curve
from sklearn.metrics import auc as calculate_auc
from sklearn.metrics import mean_squared_error
from sklearn.metrics import accuracy_score
import tensorflow as tf
import os
import numpy as np


from scipy.stats.stats import pearsonr
def r2_score(x,y):
    pcc, _ = pearsonr(x,y)
    return pcc**2

def prc_auc_score(y_true, y_score):
    precision, recall, threshold  = precision_recall_curve(y_true, y_score) #PRC_AUC
    auc = calculate_auc(recall, precision)
    return auc

'''
for early-stopping techniques in regression and classification task
'''
######## Regression ###############################


class Reg_EarlyStoppingAndPerformance(tf.keras.callbacks.Callback):

    def __init__(self, train_data, valid_data, y_scaler, MASK = -1e10, patience=5, criteria = 'val_loss', verbose = 0, batch_size = 128):
        """
        y_scaler: None, sklearn MinMaxScaler, or StandardScaler
        """
        super(Reg_EarlyStoppingAndPerformance, self).__init__()
        
        assert criteria in ['val_loss', 'val_r2'], 'not support %s ! only %s' % (criteria, ['val_loss', 'val_r2'])
        self.x, self.y  = train_data
        self.x_val, self.y_val = valid_data
        self.y_scaler = y_scaler
        
        self.history = {'loss':[],
                        'val_loss':[],
                        
                        'rmse':[],
                        'val_rmse':[],
                        
                        'r2':[],
                        'val_r2':[],
                        
                        'epoch':[]}
        self.MASK = MASK
        self.patience = patience
        # best_weights to store the weights at which the minimum loss occurs.
        self.best_weights = None
        self.criteria = criteria
        self.best_epoch = 0
        self.verbose = verbose
        self.batch_size = batch_size
        
    def rmse(self, y_true, y_pred, inner_y_true = True):
        
        if self.y_scaler != None:
            if inner_y_true:
                y_pred = self.y_scaler.inverse_transform(y_pred)
                y_true = self.y_scaler.inverse_transform(y_true)
            else:
                y_pred = self.y_scaler.inverse_transform(y_pred)
       
        N_classes = y_pred.shape[1]
        rmses = []
        for i in range(N_classes):
            y_pred_one_class = y_pred[:,i]
            y_true_one_class = y_true[:, i]
            mask = ~(y_true_one_class == self.MASK)
            mse = mean_squared_error(y_true_one_class[mask], y_pred_one_class[mask])
            rmse = np.sqrt(mse)
            rmses.append(rmse)
        return rmses   
    
    
    def r2(self, y_true, y_pred, inner_y_true = True):
        if self.y_scaler != None:
            if inner_y_true:
                y_pred = self.y_scaler.inverse_transform(y_pred)
                y_true = self.y_scaler.inverse_transform(y_true)
            else:
                y_pred = self.y_scaler.inverse_transform(y_pred)
                
        N_classes = y_pred.shape[1]
        r2s = []
        for i in range(N_classes):
            y_pred_one_class = y_pred[:,i]
            y_true_one_class = y_true[:, i]
            mask = ~(y_true_one_class == self.MASK)
            r2 = r2_score(y_true_one_class[mask], y_pred_one_class[mask])
            r2s.append(r2)
        return r2s   
    
        
    def on_train_begin(self, logs=None):
        # The number of epoch it has waited when loss is no longer minimum.
        self.wait = 0
        # The epoch the training stops at.
        self.stopped_epoch = 0
        # Initialize the best as infinity.
        if self.criteria == 'val_loss':
            self.best = np.Inf  
        else:
            self.best = -np.Inf

 
        
    def on_epoch_end(self, epoch, logs={}):
        
        y_pred = self.model.predict(self.x, verbose=0, batch_size=self.batch_size)
        rmse_list = self.rmse(self.y, y_pred)
        rmse_mean = np.nanmean(rmse_list)
        
        r2_list = self.r2(self.y, y_pred) 
        r2_mean = np.nanmean(r2_list)
        
        
        y_pred_val = self.model.predict(self.x_val, verbose=0, batch_size=self.batch_size)
        rmse_list_val = self.rmse(self.y_val, y_pred_val)        
        rmse_mean_val = np.nanmean(rmse_list_val)
        
        r2_list_val = self.r2(self.y_val, y_pred_val)       
        r2_mean_val = np.nanmean(r2_list_val)        
        
        self.history['loss'].append(logs.get('loss'))
        self.history['val_loss'].append(logs.get('val_loss'))
        
        self.history['rmse'].append(rmse_mean)
        self.history['val_rmse'].append(rmse_mean_val)
        
        self.history['r2'].append(r2_mean)
        self.history['val_r2'].append(r2_mean_val)        
        
        self.history['epoch'].append(epoch)
        
        
        # logs is a dictionary
        eph = str(epoch+1).zfill(4)   
        loss = '{0:.4f}'.format((logs.get('loss')))
        val_loss = '{0:.4f}'.format((logs.get('val_loss')))
        rmse = '{0:.4f}'.format(rmse_mean)
        rmse_val = '{0:.4f}'.format(rmse_mean_val)
        r2_mean = '{0:.4f}'.format(r2_mean)
        r2_mean_val = '{0:.4f}'.format(r2_mean_val)
        
        if self.verbose:
            print('\repoch: %s, loss: %s - val_loss: %s; rmse: %s - rmse_val: %s;  r2: %s - r2_val: %s' % (eph,
                                                                                                           loss, val_loss, 
                                                                                                           rmse,rmse_val,
                                                                                                           r2_mean,r2_mean_val),
                  end=100*' '+'\n')


        if self.criteria == 'val_loss':
            current = logs.get(self.criteria)
            if current <= self.best:
                self.best = current
                self.wait = 0
                # Record the best weights if current results is better (less).
                self.best_weights = self.model.get_weights()
                self.best_epoch = epoch

            else:
                self.wait += 1
                if self.wait >= self.patience:
                    self.stopped_epoch = epoch
                    self.model.stop_training = True
                    print('\nRestoring model weights from the end of the best epoch.')
                    self.model.set_weights(self.best_weights)    
                    
        else:
            current = np.nanmean(r2_list_val)
            
            if current >= self.best:
                self.best = current
                self.wait = 0
                # Record the best weights if current results is better (less).
                self.best_weights = self.model.get_weights()
                self.best_epoch = epoch

            else:
                self.wait += 1
                if self.wait >= self.patience:
                    self.stopped_epoch = epoch
                    self.model.stop_training = True
                    print('\nRestoring model weights from the end of the best epoch.')
                    self.model.set_weights(self.best_weights)              
    
    def on_train_end(self, logs=None):
        self.model.set_weights(self.best_weights)
        if self.stopped_epoch > 0:
            print('\nEpoch %05d: early stopping' % (self.stopped_epoch + 1))

        
        
    def evaluate(self, testX, testY):
        """evalulate, return rmse and r2"""
        y_pred = self.model.predict(testX, verbose=0, batch_size=self.batch_size)
        rmse_list = self.rmse(testY, y_pred, inner_y_true = False)
        r2_list = self.r2(testY, y_pred, inner_y_true = False)
        return rmse_list, r2_list       



    
    
######## classification ###############################

class CLA_EarlyStoppingAndPerformance(tf.keras.callbacks.Callback):

    def __init__(self, train_data, valid_data, MASK = -1, patience=5, criteria = 'val_loss', metric = 'ROC', last_avf = None, verbose = 0, batch_size = 128):
        super(CLA_EarlyStoppingAndPerformance, self).__init__()
        
        sp = ['val_loss', 'val_auc']
        assert criteria in sp, 'not support %s ! only %s' % (criteria, sp)
        self.x, self.y  = train_data
        self.x_val, self.y_val = valid_data
        self.last_avf = last_avf
        
        self.history = {'loss':[],
                        'val_loss':[],
                        'auc':[],
                        'val_auc':[],
                        
                        'epoch':[]}
        self.MASK = MASK
        self.patience = patience
        # best_weights to store the weights at which the minimum loss occurs.
        self.best_weights = None
        self.criteria = criteria
        self.metric = metric
        self.best_epoch = 0
        self.verbose = verbose
        self.batch_size = batch_size
        
        
    def sigmoid(self, x):
        s = 1/(1+np.exp(-x))
        return s

    
    def roc_auc(self, y_true, y_pred):
        if self.last_avf == None:
            y_pred_logits = self.sigmoid(y_pred)
        else:
            y_pred_logits = y_pred
            
        N_classes = y_pred_logits.shape[1]

        aucs = []
        for i in range(N_classes):
            y_pred_one_class = y_pred_logits[:,i]
            y_true_one_class = y_true[:, i]
            mask = ~(y_true_one_class == self.MASK)
            try:
                if self.metric == 'ROC':
                    auc = roc_auc_score(y_true_one_class[mask], y_pred_one_class[mask]) #ROC_AUC
                elif self.metric == 'PRC': 
                    auc = prc_auc_score(y_true_one_class[mask], y_pred_one_class[mask]) #PRC_AUC
                elif self.metric == 'ACC':
                    auc = accuracy_score(y_true_one_class[mask], np.round(y_pred_one_class[mask])) #ACC
            except:
                auc = np.nan
            aucs.append(auc)
        return aucs  
    
        
        
    def on_train_begin(self, logs=None):
        # The number of epoch it has waited when loss is no longer minimum.
        self.wait = 0
        # The epoch the training stops at.
        self.stopped_epoch = 0
        # Initialize the best as infinity.
        if self.criteria == 'val_loss':
            self.best = np.Inf  
        else:
            self.best = -np.Inf
            

        
 
        
    def on_epoch_end(self, epoch, logs={}):
        
        y_pred = self.model.predict(self.x, verbose=0, batch_size=self.batch_size)
        roc_list = self.roc_auc(self.y, y_pred)
        roc_mean = np.nanmean(roc_list)
        
        y_pred_val = self.model.predict(self.x_val, verbose=0, batch_size=self.batch_size)
        roc_val_list = self.roc_auc(self.y_val, y_pred_val)        
        roc_val_mean = np.nanmean(roc_val_list)
        
        self.history['loss'].append(logs.get('loss'))
        self.history['val_loss'].append(logs.get('val_loss'))
        self.history['auc'].append(roc_mean)
        self.history['val_auc'].append(roc_val_mean)
        self.history['epoch'].append(epoch)
        
        
        eph = str(epoch+1).zfill(4)        
        loss = '{0:.4f}'.format((logs.get('loss')))
        val_loss = '{0:.4f}'.format((logs.get('val_loss')))
        auc = '{0:.4f}'.format(roc_mean)
        auc_val = '{0:.4f}'.format(roc_val_mean)    
        
        if self.verbose:
            if self.metric == 'ACC':
                print('\repoch: %s, loss: %s - val_loss: %s; acc: %s - val_acc: %s' % (eph,
                                                                                   loss, 
                                                                                   val_loss, 
                                                                                   auc,
                                                                                   auc_val), end=100*' '+'\n')

            else:
                print('\repoch: %s, loss: %s - val_loss: %s; auc: %s - val_auc: %s' % (eph,
                                                                                   loss, 
                                                                                   val_loss, 
                                                                                   auc,
                                                                                   auc_val), end=100*' '+'\n')


        if self.criteria == 'val_loss':
            current = logs.get(self.criteria)
            if current <= self.best:
                self.best = current
                self.wait = 0
                # Record the best weights if current results is better (less).
                self.best_weights = self.model.get_weights()
                self.best_epoch = epoch

            else:
                self.wait += 1
                if self.wait >= self.patience:
                    self.stopped_epoch = epoch
                    self.model.stop_training = True
                    print('\nRestoring model weights from the end of the best epoch.')
                    self.model.set_weights(self.best_weights)    
                    
        else:
            current = roc_val_mean
            if current >= self.best:
                self.best = current
                self.wait = 0
                # Record the best weights if current results is better (less).
                self.best_weights = self.model.get_weights()
                self.best_epoch = epoch

            else:
                self.wait += 1
                if self.wait >= self.patience:
                    self.stopped_epoch = epoch
                    self.model.stop_training = True
                    print('\nRestoring model weights from the end of the best epoch.')
                    self.model.set_weights(self.best_weights)              
    
    def on_train_end(self, logs=None):
        self.model.set_weights(self.best_weights)
        if self.stopped_epoch > 0:
            print('\nEpoch %05d: early stopping' % (self.stopped_epoch + 1))

        
    def evaluate(self, testX, testY):
        
        y_pred = self.model.predict(testX, verbose=0, batch_size=self.batch_size)
        roc_list = self.roc_auc(testY, y_pred)
        return roc_list            

            
