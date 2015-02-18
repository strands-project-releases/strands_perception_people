#include <iostream>
#include <string>

#include "json/json.h"

#include "dists.hpp"
#include "filterbank.hpp"
#include "mainutils.hpp"
#include "warco.hpp"

int main(int argc, char** argv)
{
    if(argc != 3) {
        std::cout << "Usage: " << argv[0] << " CONF_FILE MODEL_NAME" << std::endl;
        std::cout << std::endl;
        std::cout << "CONF_FILE  Path to the JSON config file describing the dataset." << std::endl;
        std::cout << "MODEL_NAME Name of the model which should be save. Is a directory." << std::endl;
        return 0;
    }

    Json::Value dataset = warco::readJson(argv[1]);
    auto patches = warco::readPatches(dataset);
    auto fb = cv::FilterBank(dataset["filterbank"].asCString());
    auto dfn = dataset.get("dist", "cbh").asString();
    warco::Warco model(fb, patches, "cbh");

    std::cout << "Loading images... " << std::flush;
    warco::foreach_img(dataset, "train", [&model](unsigned lbl, const cv::Mat& image, std::string) {
        model.add_sample(image, lbl);
    });
    std::cout << "Done" << std::endl;

    bool cov = dataset.get("cov", "true").asBool();

    std::cout << "Computing " << (cov ? "covs" : "corrs") << " with:" << std::endl
        << "- filterbank: " << dataset["filterbank"].asString() << std::endl
        << "- #patches: " << patches.size() << std::endl;

    if(!cov)
        model.prepare();

    model.save_covs(argv[2]);

    std::cout << "Done. Cya in predictions!" << std::endl;

    return 0;
}

