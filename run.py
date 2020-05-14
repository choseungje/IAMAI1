from home_model import iamai


run = iamai()
run.load_img()
run.create_y()
run.data_pretreatment()
run.create_model()
