import os
import hover
from hover.workflow import Automated
from hover.utils.public_dataset import newsgroups_dictl
from hover.future.core.dataset import SupervisableTextDataset

# define functions that provide crucial intermediates
def create_workflow():
    data_home = os.path.join(os.path.dirname(__file__), '../scikit_learn_data/')
    my_20ng, label_encoder, label_decoder = newsgroups_dictl(data_home=data_home)

    # taking a small subset of the data so that the Binder example loads faster
    split_idx = int(0.1 * len(my_20ng["train"]))
    #split_idx = int(0.9 * len(my_20ng["train"]))
    dataset = SupervisableTextDataset(
        raw_dictl=my_20ng["train"][:split_idx],
        dev_dictl=my_20ng["train"][split_idx:int(split_idx * 1.2)],
        #dev_dictl=my_20ng["train"][split_idx:],
        test_dictl=my_20ng["test"],
    )

    dataset.dfs["raw"].drop(["label"], inplace=True, axis=1)
    dataset.synchronize_df_to_dictl()

    workflow = Automated(dataset=dataset, model_module_name="model_template")
    workflow.compute_text_to_2d("umap")

    return workflow

def link_plots(*explorers):
    linked_plots = [
        *explorers,
    ]
    
    for i, _pi in enumerate(linked_plots):
        # set plots to the same size
        _pi.figure.plot_height = 600
        _pi.figure.plot_width = 800
        for j, _pj in enumerate(linked_plots):
            if not i == j:
                # link coordinate ranges
                for _attr in ["start", "end"]:
                    _pi.figure.x_range.js_link(
                        _attr, _pj.figure.x_range, _attr,
                    )
                    _pi.figure.y_range.js_link(
                        _attr, _pj.figure.y_range, _attr,
                    )
                # link selection
                _pi.source.selected.js_link(
                    "indices", _pj.source.selected, "indices"
                )
                
    return linked_plots