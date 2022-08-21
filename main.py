import click
import time
import pandas as pd

@click.command()
def export():
    click.echo("Opening file...")
    frame = pd.read_excel("IW.xlsx")
    with click.progressbar(length=len(frame.index)) as bar:        
        baza = pd.read_csv("BAZA.csv", delimiter=';').drop('Unnamed: 2', axis=1)
        db_KodTowarowy = list(baza["KodTowarowy"])
        db_OpisTowaru = list(baza["OpisTowaru"])
        for index in frame.index:
            kod = frame.loc[index, 'KodTowarowy']
            try:
                kodTowarowy = int(str(kod)[:8:])
            except ValueError:
                kodTowarowy = 0
            if kodTowarowy in db_KodTowarowy:
                i = db_KodTowarowy.index(kodTowarowy)
                frame.loc[index, 'KodTowarowy'] = db_KodTowarowy[i]
                frame.loc[index, 'OpisTowaru'] = db_OpisTowaru[i]
            bar.update(index)
        click.echo("\nSaving file...")
        frame.to_excel("ready.xlsx", index=False)
    

@click.command()
@click.option('-b', '--blue', is_flag=True, help='message in blue color')
@click.option('-y', '--yellow', is_flag=True, help='message in yellow color')
def hello(blue, yellow):
    global color
    color = None
    if blue:
        color = "blue"
    if yellow:
        color = "yellow"
    click.secho("Hello world", fg=color)
       
 
if __name__ == '__main__':
    export()

    