function updateLengthsPerSec() {
    let speedA = parseFloat(document.querySelector('input[name="speed_a"]').value) || 0;
    let lengthA = parseFloat(document.querySelector('input[name="length_a"]').value) || 1;
    let speedB = parseFloat(document.querySelector('input[name="speed_b"]').value) || 0;
    let lengthB = parseFloat(document.querySelector('input[name="length_b"]').value) || 1;

    document.querySelector('#lengths_sec_a').textContent = (speedA / lengthA).toFixed(2);
    document.querySelector('#lengths_sec_b').textContent = (speedB / lengthB).toFixed(2);
}

document.querySelectorAll('input[name="speed_a"], input[name="length_a"], input[name="speed_b"], input[name="length_b"]').forEach(el => {
    el.addEventListener('input', updateLengthsPerSec);
});

updateLengthsPerSec();
