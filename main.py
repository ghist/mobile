from kivy.app import App
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.core.window import Window
from kivy.graphics import Color, Ellipse, Rectangle
from kivy.properties import ListProperty
from kivy.animation import Animation
import json

class Gerenciador(ScreenManager):
    pass


class Menu(Screen):
    def on_pre_enter(self):
        Window.bind(on_request_close=self.confirmacao)
    
    
    def confirmacao(self,*args,**kwargs):
        box = BoxLayout(orientation='vertical', padding=10,spacing=10)
        botoes = BoxLayout(padding=10,spacing=10)
        
        pop = Popup(title='Deseja sair?',content=box,size_hint=(None,None),
                    size=(200,150))
        
        sim = Botao(text='Sim',on_release=App.get_running_app().stop)
        nao = Botao(text='Não',on_release=pop.dismiss)
        
        botoes.add_widget(sim)
        botoes.add_widget(nao)
        
        box.add_widget(botoes)
        
        animText = Animation(color=(0.2,0.9,0.5,1)) + Animation(color=(0,0,0,1)) + Animation(color=(0.3,0.8,0.1,1))
        animText.repeat = True
        animText.start(sim)
        pop.open()
        return True
        
class Botao(ButtonBehavior,Label):
    cor = ListProperty([0.5,0.3,0.8,1])
    cor2 = ListProperty([0.1,0.1,0.1,1])
    
    def __init__(self,**kwargs):
        super(Botao,self).__init__(**kwargs)
        self.atualizar()
        
    def on_pos(self,*args):
        self.atualizar()
        
    def on_size(self,*args):
        self.atualizar()
        
    def on_press(self,*args):
        self.cor, self.cor2 = self.cor2, self.cor
    
    def on_release(self,*args):
        self.cor, self.cor2 = self.cor2, self.cor
    
    def on_cor(self,*args):
        self.atualizar()
        
    def atualizar(self,*args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(rgba=self.cor)
            Ellipse(size=(self.height,self.height),
                    pos=self.pos)
            Ellipse(size=(self.height,self.height),
                    pos=(self.x+self.width-self.height,self.y))
            Rectangle(size=(self.width-self.height,self.height),
                    pos=(self.x+self.height/2.0,self.y))

class Tarefas(Screen):
    tarefas = []
    path = ''
            
    def on_pre_enter(self):
        self.ids.box.clear_widgets()
        self.path = App.get_running_app().user_data_dir+'/'
        self.loadData()
        Window.bind(on_keyboard=self.voltar)
        for tarefa in self.tarefas:
            self.ids.box.add_widget(Tarefa(text=tarefa))
        
    def voltar(self,window,key,*args):
        if key == 27:
            App.get_running_app().root.current = 'menu'
            return True
            
    def on_pre_leave(self):
        Window.unbind(on_keyboard=self.voltar)
        
    def loadData(self,*args):
        try:
            with open(self.path+'data.json', 'r') as data:
                self.tarefas = json.load(data)
        except FileNotFoundError:
            pass
        
    def saveData(self,*args):
        with open(self.path+'data.json', 'w') as data:
            json.dump(self.tarefas,data)
            
    def removeWidget(self, tarefa):
        texto = tarefa.ids.label.text
        self.ids.box.remove_widget(tarefa)
        self.tarefas.remove(texto)
        self.saveData()
            
    def addWidget(self):
        texto = self.ids.texto.text
        self.ids.box.add_widget(Tarefa(text=texto))
        self.ids.texto.text = ''
        self.tarefas.append(texto)
        self.saveData()
        

class Tarefa(BoxLayout):
    def __init__(self, text='', **kwargs):
        super().__init__(**kwargs)
        self.ids.label.text= text


class Teste(App):
    def build(self):
        return Gerenciador()
    
    
Teste().run()