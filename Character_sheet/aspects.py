from addict import Dict

char = Dict()

char.info.update({'alignment' : None, 
                'level' : None, 
                'name' : None,
                'race' : None,
                'size' : Dict({'race' : {}, 'temp' : {}}),
                'speed' : Dict({'race' : {}, 'mod' : {}})
                })

char.bio.update({'faith' : None
                })

char.profficiencies.update({'languages' : Dict(), 
                'armor' : Dict(),
                'weapons' : Dict()
                })

char.stats.update({'max_hp' : None,
                'current_hp' : None,
                'armour_class' : None})

char.actions.update({'actions' : Dict(),
                'bonus' : Dict(),
                'attack' : Dict(),
                'reaction' : Dict()})


        # self.bio = Bio()
        # self.profficiencies = Profficiencies()
        # self.saving_throws = Saving_Throws()
        # self.feats = Empty()
        # self.actions = Actions()
        # self.role_play = Empty()        
        # self.stats = Stats()
        # self.attributes = Attributes()
        # self.skills = skills()
print("Done!")