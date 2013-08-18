'''
Created on Aug 7, 2013

@author: Morgan Redshaw and Neil Borle
'''

import PySide.QtCore as QtCore
import createdMenu
from PySide.QtGui import QWidget, QIcon, QPixmap

class PreferencesButton(QWidget, createdMenu.Ui_menuBackground):
    '''
    classdocs
    '''

    def __init__(self, parent=None):
        '''
        This determines what should happen when the buttons are clicked
        buttons are:
        starButton
        constellationButton
        messierButton
        planetsButton
        meteorButton
        gridButton
        horizonButton
        '''
        super(PreferencesButton, self).__init__(parent)
        self.setupUi(PreferencesButton)

        self.starButtonActive = True
        self.constellationButtonActive = True
        self.messierButtonActive = True
        self.planetsButtonActive = True
        self.meteorButtonActive = True
        self.gridButtonActive = True
        self.horizonButtonActive = True
    
    def checkForButtonPress(self, source, event):
        
        if event.type() != QtCore.QEvent.MouseButtonPress:
            return False
        
        if source == self.starButton:
            self.StarButtonClicked()
            return ["source_provider.0"]
        
        elif source == self.constellationButton:
            self.ConstellationButtonClicked()
            return ["source_provider.1"]
            
        elif source == self.messierButton:
            self.MessierButtonClicked()
            return ["source_provider.2"]
            
        elif source == self.planetsButton:
            self.PlanetButtonClicked()
            return ["source_provider.3"]
        
        elif source == self.meteorButton:
            self.MeteorButtonClicked()
            return ["source_provider.7"]
        
        elif source == self.gridButton:
            self.GridButtonClicked()
            return ["source_provider.4", "source_provider.5"]
        
        elif source == self.horizonButton:
            self.HorizonButtonClicked()
            return ["source_provider.6"]
            
        else:
            return False

    def StarButtonClicked(self):   
        if self.starButtonActive:
            imageOpen = "star_off"
            
        else:
            imageOpen = "star_on"
    
        self.ChangeButton(self.starButton, imageOpen)
        self.starButtonActive = not self.starButtonActive
    
    def ConstellationButtonClicked(self):        
        if self.constellationButtonActive:
            imageOpen = "stars_off"
            
        else:
            imageOpen = "stars_on"
    
        self.ChangeButton(self.constellationButton, imageOpen)
        self.constellationButtonActive = not self.constellationButtonActive
        
    def MessierButtonClicked(self):        
        if self.messierButtonActive:
            imageOpen = "messier_off"
            
        else:
            imageOpen = "messier_on"
    
        self.ChangeButton(self.messierButton, imageOpen)
        self.messierButtonActive = not self.messierButtonActive
    
    def PlanetButtonClicked(self):        
        if self.planetsButtonActive:
            imageOpen = "planet_off"
            
        else:
            imageOpen = "planet_on"
    
        self.ChangeButton(self.planetsButton, imageOpen)
        self.planetsButtonActive = not self.planetsButtonActive
        
    def MeteorButtonClicked(self):        
        if self.meteorButtonActive:
            imageOpen = "b_meteor_off"
            
        else:
            imageOpen = "b_meteor_on"
    
        self.ChangeButton(self.meteorButton, imageOpen)
        self.meteorButtonActive = not self.meteorButtonActive
        
    def GridButtonClicked(self):        
        if self.gridButtonActive:
            imageOpen = "grid_off"
            
        else:
            imageOpen = "grid_on"
    
        self.ChangeButton(self.gridButton, imageOpen)
        self.gridButtonActive = not self.gridButtonActive
        
    def HorizonButtonClicked(self):        
        if self.horizonButtonActive:
            imageOpen = "horizon_off"
            
        else:
            imageOpen = "horizon_on"
    
        self.ChangeButton(self.horizonButton, imageOpen)
        self.horizonButtonActive = not self.horizonButtonActive

    def ChangeButton(self, buttonChosen, imageOpen):        
        icon = QIcon()
        icon.addPixmap(QPixmap(":/icons/assets/drawable/" + imageOpen + ".png"), QIcon.Normal, QIcon.Off)
        buttonChosen.setIcon(icon) 

    
    
    