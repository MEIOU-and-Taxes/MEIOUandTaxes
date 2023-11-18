import glob

if __name__ == '__main__':
    for path in glob.glob('common\\countries\\*.txt'):
        with open(path, encoding='ISO-8859-1') as f:
            t = f.read()

            t = t.replace('logistic_ideas', 'logistics_ideas')
            t = t.replace('spy_ideas', 'espionage_ideas')
            t = t.replace('democracy_ideas', 'representation_ideas')
            t = t.replace('asceticism_ideas', '#asceticism_ideas')
            t = t.replace('ceremony_ideas', '#ceremony_ideas')
            t = t.replace('diplomatic_ideas', 'diplomacy_ideas')
            t = t.replace('mercenary_ideas_2', '#mercenary_ideas_2')
            t = t.replace('merchant_marine_ideas', '#merchant_marine_ideas')
            t = t.replace('popular_religion_ideas', '#popular_religion_ideas')
            t = t.replace('scholasticism_ideas', '#scholasticism_ideas')
            t = t.replace('theology_ideas', '#theology_ideas')

            with open(path, 'w', encoding='ISO-8859-1') as ff:
                ff.write(t)
