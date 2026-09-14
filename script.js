const GRID_SIZE = 8;
const BITS_COUNT = 64;
const HEX_LENGTH = 16;

const grid = document.getElementById('sprite-grid');
const hexOutput = document.getElementById('hex-output');
const hexInput = document.getElementById('hex-input');
const loadHexBtn = document.getElementById('load-hex-btn');
const errorText = document.getElementById('error-text');

const pixelStates = Array(BITS_COUNT).fill(false);
const pixelButtons = [];

function setError(message) {
  errorText.textContent = message;
}

function clearError() {
  errorText.textContent = '';
}

function updateHexOutput() {
  const binaryString = pixelStates.map((active) => (active ? '1' : '0')).join('');
  const decimalValue = parseInt(binaryString, 2);
  hexOutput.textContent = decimalValue.toString(16).toUpperCase().padStart(HEX_LENGTH, '0');
}

function updateGridVisuals() {
  pixelButtons.forEach((button, index) => {
    button.classList.toggle('on', pixelStates[index]);
  });
}

function togglePixel(index) {
  pixelStates[index] = !pixelStates[index];
  updateGridVisuals();
  updateHexOutput();
}

function createGrid() {
  for (let index = 0; index < BITS_COUNT; index += 1) {
    const button = document.createElement('button');
    button.type = 'button';
    button.className = 'pixel';
    button.setAttribute('aria-label', `Pixel ${index + 1}`);
    button.addEventListener('click', () => togglePixel(index));
    grid.appendChild(button);
    pixelButtons.push(button);
  }

  updateGridVisuals();
  updateHexOutput();
}

function loadHexToGrid() {
  const rawValue = hexInput.value.trim().toUpperCase();
  clearError();

  if (!rawValue) {
    setError('Por favor, ingresa un valor Hexadecimal.');
    return;
  }

  if (!/^[0-9A-F]+$/.test(rawValue)) {
    setError('Entrada inválida. Usa solo caracteres Hexadecimales (0-9, A-F).');
    return;
  }

  if (rawValue.length > HEX_LENGTH) {
    setError('El valor excede el límite de 64 bits (16 dígitos hex).');
    return;
  }

  const decimalValue = parseInt(rawValue, 16);
  const binaryString = decimalValue.toString(2).padStart(BITS_COUNT, '0');

  for (let index = 0; index < BITS_COUNT; index += 1) {
    pixelStates[index] = binaryString[index] === '1';
  }

  updateGridVisuals();
  updateHexOutput();
  hexInput.value = '';
  hexInput.focus();
}

loadHexBtn.addEventListener('click', loadHexToGrid);

hexInput.addEventListener('keydown', (event) => {
  if (event.key === 'Enter') {
    loadHexToGrid();
  }
});

createGrid();
