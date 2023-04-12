import json
from pathlib import Path
import shutil
def main ():
    student = {
        'name': 'Sonia',
        'surname': 'Zakharova',
        'hobbies' : [
              'sport',
              'reading',
        ]
    }




    with open('./sample.json', 'w', encoding='utf-8') as f:
        json.dump(student, f, ensure_ascii=True,
                  indent=4)

    with open('./sample.json', 'r', encoding='utf-8') as f:
        content = json.load(f)
    print(content)
    print(type(content))

    sample_path = Path('sample.json')
    sample_path = Path ('C:/Users/Соник/Desktop/учеба/2022-2-level-ctlr/seminars/03/main1.py')
    sample_path = Path('.')
    print(sample_path.resolve()) #absolute path

    sample_path = Path (__file__).parent / 'sample.json'
    print(sample_path)

    config_path = (
        Path(__file__).parent.parent.parent /
        'lab_5_scrapper' /
        'scrapper_config.json')
    print(config_path)
    print(config_path.exists())

    sample_dir_path = Path(__file__).parent / 'data' / 'assests'
    print(sample_dir_path.exists())
    sample_dir_path.mkdir(exist_ok=True, parents=True)


    with open(sample_dir_path / '1.txt', 'w') as f:
        f.write("Hello")

    #sample_txt_path = sample_dir_path / '1.txt'
    #with sample_txt_path.open('w') as f:
    #f.write('Hello')
    #КАК С ТЕРМИНАЛА ОТКРЫТЬ НАУЧИТЕСЬ

    #shutil.rmtree(sample_dir_path)

    current_directory_path = Path(__file__).parent
    for file_instance in current_directory_path.glob('*.py'):
        print(file_instance)

    #sample_dir_path.rmdir() # empty dir removes


if __name__ == '__main__':
        main()
