from frex.utils import ClassGenerator
from pathlib import Path


def test_class_generation(
):
    test_onto = 'examples/ramen_rec/data/cr.nt'
    test_onto = str(Path(test_onto).resolve())
    # test_onto = "https://raw.githubusercontent.com/tetherless-world/ontology-engineering/course-recommender/oe2020/course-recommender/course-recommender.rdf"
    test_onto = "https://raw.githubusercontent.com/tetherless-world/explanation-ontology/master/Ontologies/explanation-ontology.owl"
    test_dir_name = 'test_models/'
    Path(test_dir_name).mkdir(parents=True, exist_ok=True)
    test_dir = Path(test_dir_name).resolve()
    cg = ClassGenerator(onto_file=test_onto, save_dir=test_dir)
    cg.generate()
    print(test_dir)
    #test_dir.rmdir()
