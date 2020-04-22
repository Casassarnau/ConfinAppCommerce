
const updateSliderLab = value => {
    const label = document.getElementById("sliderLab-meanTime");

    const real_slider = document.getElementById("id_meanTime");

    if (value == 60) {
        label.textContent = "1 h";
    } else {
        label.textContent = value + " min";
    }

    real_slider.value = value;
};
