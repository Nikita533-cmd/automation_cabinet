import * as THREE from 'three';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';


console.log("Жопа")

// !!!!!!!!!!!!!!!!!!!!!!!!!!!!!СЛУШАТЕЛИ!!!!!!!!!!!!!!!!!!!!!!!!!!!
const count_outlet = document.getElementById(`outlet`);
const count_output = document.getElementById('count_outlet') 
console.log('count_outlet:', count_outlet);
count_outlet.addEventListener('change', (event) => {
  const value = parseInt(event.target.value, 10); 
  if (!isNaN(value)) { 
    console.log('value:', value)
    // create_outlet(value);      
    count_output.innerHTML = '';
    count_output.innerHTML = create_outlet(value);
  }
});



// Функция для создания HTML контента отводящих элементов
function create_outlet(i) {
    let create_outlet = '';
    

    for (let j = 1; j <= i; j++) {               
        

        create_outlet += `

        <table class="parameters">
            <colgroup>
                <col style="width: 45%;">
                <col style="width: 25%;">
                <col style="width: 15%;">
                <col style="width: 15%;">
            </colgroup>
            <tr id="row1">
                <td style="text-align: left; padding-left: 0px;">
                    <label class="form-label">
                         Отводящая линия № ${j}
                    </label>
                </td>
                <td style="text-align: right;">
                    <input type="number" class="form-control" id="power_outlet_${j}" name="power_outlet_${j}" required min="1" max="95" oninput="if(parseFloat(this.value) > 95) this.value = 95;">
                </td>
                <td style="text-align: left;">А</td>
                <td id="recalculation" style="text-align: left;">-</td>
            </tr>                    
        </table>    
        
        
        `;        
    }
    return create_outlet;

}

// !!!!!!!!!!!!!!!!!!!!!!!!!РАСЧЕТ - ПОДБОР !!!!!!!!!!!!!!!!!!!!!
const calculation_Button = document.getElementById('calculation');

calculation_Button.addEventListener('click', async function(e) {
     e.preventDefault(); 

    const inputForm = document.getElementById('input_form'); 
  
//   const powerInput = document.getElementById('power');
//   const countSelect = document.getElementById('count');
    const checkboxAVR = document.getElementById('checkbox_AVR'); 
//   const outletInput = document.getElementById('outlet');
//   
//   if (!powerInput.value) {
//     alert("Не указана пропускная мощность щита! Пожалуйста, введите значение перед запуском расчета.");
//     powerInput.focus();
//     return;
//   }

//   if (!countSelect.value) {
//     alert("Не указано количество вводов! Пожалуйста, выберите значение из списка перед запуском расчета.");
//     countSelect.focus();
//     return;
//   }

//   if (!outletInput.value) {
//     alert("Не указано количество отводящих линий! Пожалуйста, введите значение перед запуском расчета.");
//     outletInput.focus();
//     return;
//   }
  
// 1. Проверяем валидность формы средствами HTML5
    const isValid = this.checkValidity(); 

    if (!isValid) {
        // Добавляем класс Bootstrap, который заставит все невалидные поля загореться красным
        this.classList.add('was-validated');

        // Находим самое первое поле с ошибкой на странице
        const firstInvalidElement = this.querySelector('input:invalid, select:invalid, textarea:invalid');
        
        if (firstInvalidElement) {
            // Плавно скроллим к элементу, который заполнен неверно
            firstInvalidElement.scrollIntoView({ behavior: 'smooth', block: 'center' });
            // Ставим на него фокус
            firstInvalidElement.focus();
        }
        alert("Подбор не выполнен! Пожалуйста, проверьте заполнение полей на странице. Некоторые обязательные ячейки не заполнены или содержат некорректные значения (выделены красным).");
        return; // Останавливаем выполнение, fetch не вызовется
    }

    // Если форма валидна, убираем класс прошлых ошибок (на случай повторной отправки)
    this.classList.remove('was-validated');  

    // Собираем данные формы
    const formData = new FormData(inputForm);
    const dataObject = Object.fromEntries(formData.entries());

    // Добавляем состояние чекбокса вручную (FormData не включает неотмеченные чекбоксы)
    dataObject.checkbox_AVR = checkboxAVR.checked ? 'on' : 'off';
    formData.set('checkbox_AVR', checkboxAVR.checked);
    var dq = {}
    console.log('--- FormData ---');
    for (const [key, value] of formData.entries()) {
        console.log(`${key}: ${value}`);
        dq[key]=value;
    }
    console.log('--- Конец FormData ---', dq);

    console.log(formData);
    const token = localStorage.getItem('access_token');
    const response = await fetch('api/test/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                ...(token && { 'Authorization': `JWT ${token}` })
            },
            body: JSON.stringify(dq)
        });
        
        // Обработка ответа
        if (!response.ok) {
            const errors = await response.json();
            throw new Error(errors.detail || errors.message || 'Ошибка сервера');
        }
        
        const result = await response.json();
        console.log('Успех:', result);
//      console.log(`  checkbox_AVR: ${dataObject.checkbox_AVR}`);
  
});

document.getElementById("asd");





// !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! Работа с three js !!!!!!!!!!!!!!!!!!!!!!!

let SCENE;
let CAMERA;
let RENDERER;
let LOADING_MANAGER;
let GLB_LOADER;
let CONTROLS;
let MOUSE;
let MAIN_MODEL;
let ADD_MODELS = [];

main();

function main() {
    init();
    animate();
    // addButton();
}

function init() {
    initScene();
    initCamera();
    initRenderer();    
    initLoaders();
    initControls();
   
    loadModel();

   
}

function initScene() {
    SCENE = new THREE.Scene();
    SCENE.background = new THREE.Color(0x87CEEB); // Голубой фон (небо)
    initLights();
}

function initLights() {
    const ambient = new THREE.AmbientLight(0xffffff, 0.7);
    SCENE.add(ambient);

    const directionalLight = new THREE.DirectionalLight(0xffffff);
    directionalLight.position.set(0, 100, 100);
    directionalLight.castShadow = true;
    directionalLight.shadow.camera.left   = -50;
    directionalLight.shadow.camera.right  =  50;
    directionalLight.shadow.camera.top    =  50;
    directionalLight.shadow.camera.bottom = -50;

    SCENE.add(directionalLight);
}

function initCamera() {
    CAMERA = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 1, 2000);
    CAMERA.position.z = 1000;
}

function initRenderer() {
    const container = document.getElementById('okno');
    RENDERER = new THREE.WebGLRenderer({ antialias: true });
    RENDERER.setPixelRatio(window.devicePixelRatio);
    RENDERER.setSize(container.clientWidth, container.clientHeight);
    RENDERER.shadowMap.enabled = true;
    RENDERER.shadowMapSort = true;
    container.appendChild(RENDERER.domElement);
}

function initLoaders() {
    LOADING_MANAGER = new THREE.LoadingManager();

    
}

function loadModel() {
    GLB_LOADER = new GLTFLoader();
    GLB_LOADER.load(
        'static/models/sten.glb',
        function(gltf) {
            const model = gltf.scene;
            model.position.set(0, 0, 0);
            model.scale.set(1, 1, 1);
            SCENE.add(model);
            console.log('Модель загружена!');
            MAIN_MODEL = model;
            // Добавляем оси к модели
            addAxesToModel(model, 500); // Длина осей — 5 единиц
            },
        function(xhr) { console.log((xhr.loaded / xhr.total * 100) + '%'); },
        function(error) { console.error(error); }
    );
    
}

function addAxesToModel(model, axisLength = 3) {
  const axesHelper = new THREE.AxesHelper(axisLength);
  model.add(axesHelper);
}


function initControls() {

    CONTROLS = new OrbitControls(CAMERA, RENDERER.domElement);    
    CONTROLS.minPolarAngle = Math.PI * 1 / 4;
    CONTROLS.maxPolarAngle = Math.PI * 3 / 4;
    CONTROLS.minDistance = 100;
    CONTROLS.maxDistance = 1500;
    CONTROLS.autoRotate = true;
    // CONTROLS.autoRotate = false;
    CONTROLS.autoRotateSpeed = -1.0;
    CONTROLS.update();

    MOUSE = new THREE.Vector2();
}


function animate() {
    requestAnimationFrame(animate);
    CONTROLS.update();
    render();
}

function render() {
    CAMERA.lookAt(SCENE.position); 

    RENDERER.render(SCENE, CAMERA);
    
}

// // Добавить модель
// function addButton() {
//   const button = document.getElementById('button_add');
//   button.addEventListener('click', add_model);
// }

// // Функция добавления модели относительно основной
// function add_model() {

//   const position_y = parseFloat(document.getElementById('position_y').value);
//   const position_z = parseFloat(document.getElementById('position_z').value);   

//   const loader = new GLTFLoader();
//   loader.load(
//     'static/models/rele.glb', // Путь к новой модели
//     function(gltf) {
//         const newModel = gltf.scene;      
//         newModel.position.copy(MAIN_MODEL.position);
//         newModel.rotation.x = THREE.MathUtils.degToRad(90);
//         newModel.position.x += 3;   // смещение по х
//         newModel.position.y -= position_y;
//         newModel.position.z += position_z;
        
//         newModel.scale.copy(MAIN_MODEL.scale);
        
//         SCENE.add(newModel);
//         
//     },
//     function(xhr) { console.log('Загрузка новой модели: ' + (xhr.loaded / xhr.total * 100) + '%'); },
//     function(error) { console.error('Ошибка загрузки новой модели:', error); }
//   );
// }