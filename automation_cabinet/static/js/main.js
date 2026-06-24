import * as THREE from 'three';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';




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
    eventlistener_outlet(value);
    }
});

////////////////////////////////// вкл -выкл - АВР
const row4 = document.getElementById('row4'); ///////////// строка наличия АВР
const count_input = document.getElementById(`count`);
count_input.addEventListener('click', function () {
    
    if (parseInt(count_input.value, 10) === 2) {
            
        row4.style.display = 'table-row';
    }
    else {
        row4.style.display = 'none';
    }
});


///////////////////////////пересчет начальных вводов/////////////////////////////////
const power_amper = document.getElementById(`power`);
const voltage = document.getElementById(`voltage`);
const power_kvt = document.getElementById('power_kvt');
power_amper.addEventListener('change', (event) => {
    const value = parseFloat(event.target.value); 
    if (!isNaN(value)) { 
    // console.log('value 28', value)
    const kvt = value*voltage.value/1000;
    power_kvt.value = kvt.toFixed(2);
    }
});
power_kvt.addEventListener('change', (event) => {
    const value = parseFloat(event.target.value); 
    if (!isNaN(value)) { 
    // console.log('value 26', value)
    const amper = value*1000/voltage.value;
    // console.log('amper 38', amper)
    power_amper.value = amper.toFixed(2);
    }
});
voltage.addEventListener('change', (event) => {
    const changeEvent = new Event('change');
    power_amper.dispatchEvent(changeEvent);
    count_outlet.dispatchEvent(changeEvent);
});

function eventlistener_outlet(i){
    for (let j = 1; j <= i; j++) {
        const power_amper_outlet = document.getElementById(`power_outlet_${j}`);
        const power_kvt_outlet = document.getElementById(`power__outlet_kvt_${j}`);
        const voltage_outlet = document.getElementById(`voltage_outlet_${j}`);

        power_amper_outlet.addEventListener('change', (event) => {
        const value = parseFloat(event.target.value);         
        
        if (!isNaN(value)) { 
            // console.log('value 28', value)
            const kvt_outlet = value*voltage_outlet.value/1000;
            power_kvt_outlet.value = kvt_outlet.toFixed(2);
        }
        });
        power_kvt_outlet.addEventListener('change', (event) => {
        const value = parseFloat(event.target.value); 
        if (!isNaN(value)) { 
            // console.log('value 26', value)
            const amper_outlet = value*1000/voltage_outlet.value;
            // console.log('amper 38', amper)
            power_amper_outlet.value = amper_outlet.toFixed(2);
        }
        });

        voltage_outlet.addEventListener('change', (event) => {
            const changeEvent = new Event('change');
            power_amper_outlet.dispatchEvent(changeEvent);

            if (voltage.value === '220') {
                voltage_outlet.value = "220";
                power_amper_outlet.dispatchEvent(changeEvent);
                alert("Увеличьте напряжение ввода!");
            }
        });
    }

}

// Функция для создания HTML контента отводящих элементов
function create_outlet(i) {
    let create_outlet = '';
    

    for (let j = 1; j <= i; j++) {               
        

        create_outlet += `

        <table class="parameters table">
            <colgroup>
                <col style="width: 23.3%;">
                <col style="width: 10%;">
                <col style="width: 23.3%;">
                <col style="width: 10%;">
                <col style="width: 23.3%;">
                <col style="width: 10%;">
            </colgroup>
            <tr id="row1_outlet">
                <td colspan="6" style="text-align: center; >
                    <label class="form-label" >
                            Отводящая линия № ${j}
                    </label>
                </td>
            </tr>
            <tr id="row2_outlet">
                <td style="text-align: right;">
                    <select class="form-control" id="voltage_outlet_${j}" name="voltage_outlet_${j}" required>
                        <option>220</option>
                        <option>380</option>
                    </select>
                </td>
                <td style="text-align: left;">В</td>
                <td style="text-align: right;">
                    <input type="number" class="form-control" id="power_outlet_${j}" name="power_outlet_${j}" required min="1" max="95" 
                    step="0.01" oninput="if(parseFloat(this.value) > 95) this.value = 95;">
                </td>
                <td style="text-align: left;">А</td>
                <td style="text-align: right;">
                    <input type="number" class="form-control" id="power__outlet_kvt_${j}" name="power__outlet_kvt_${j}" min="0.22" max="36.10" 
                    step="0.01" oninput="const voltage = document.getElementById('voltage_outlet_${j}');
                            if (voltage) {
                                const voltage_value = parseFloat(voltage.value);
                                const value = parseFloat(this.value);                                                                
                                if (voltage_value === 220 && value > 20.90) {
                                    this.value = '20.90';
                                }                                 
                                else if (value > 36.10) {
                                    this.value = '36.10';
                                }
                            }">
                </td>
                <td id="recalculation" style="text-align: left;">кВт</td>
            </tr>                    
        </table>    
        
        
        `;        
    }
    return create_outlet;

}

// !!!!!!!!!!!!!!!!!!!!!!!!!РАСЧЕТ - ПОДБОР !!!!!!!!!!!!!!!!!!!!!
const calculation_form = document.getElementById('input_form');

calculation_form.addEventListener('submit', async function(e) {
        e.preventDefault(); 


    const inputForm = document.getElementById('input_form'); 
    const checkboxAVR = document.getElementById('checkbox_AVR'); 
    clearScene();

// 1. Проверяем валидность формы средствами HTML5
    const isValid = this.checkValidity(); 
    // alert("до валидности формы!!!!!!")
    

    if (!isValid) {
        // alert("форма не валидна!!!!!!")
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

    dataObject.checkbox_AVR = checkboxAVR.checked ? 'on' : 'off';
        formData.set('checkbox_AVR', checkboxAVR.checked);
    // Добавляем состояние чекбокса вручную (FormData не включает неотмеченные чекбоксы)
    // row4.style.display = 'table-row';
    // if (row4.style.display === "table-row") {
        // dataObject.checkbox_AVR = checkboxAVR.checked ? 'on' : 'off';
        // formData.set('checkbox_AVR', checkboxAVR.checked);
    // }
    
    const dq = { outs: [] };
    // console.log('--- FormData ---');


    for (let j = 1; j <= parseInt(document.getElementById('outlet').value, 10); j++) {
        const currentOut = {            
            name: `Отводящая линия № ${j}`,
            i: parseFloat(document.getElementById(`power_outlet_${j}`)?.value),            
            voltage: parseFloat(document.getElementById(`voltage_outlet_${j}`)?.value) 
        };
        dq.outs.push(currentOut);
    }

    for (const [key, value] of formData.entries()) {
        // console.log(`${key}: ${value}`);
        // if (key.includes("power_outlet"))
        // {
        //     dq.outs.push({name: key, i: value});
        // }
        // else if (key.includes("voltage_outlet"))
        // {
        //     dq.outs.push({name: key, u: value});
        // }
        // else {
        //     dq[key]=value;
        // }
        dq[key]=value;
    }
    console.log('--- Конец FormData ---', dq);

    // console.log(formData);
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

        
        const general_price = document.getElementById('price');
        general_price.textContent = 'Стоимость: '+ Math.round(result.price) + ' руб.';
        

        const general_mass = document.getElementById('massa'); 
        general_mass.textContent = 'Масса: ' + Math.round(result.mass) + ' кг';
        

        for (const name in result) {       

            if (name === 'cabinet') {
                const cabinet = result[name];
                
                const A = cabinet.A ?? null;
                const B = cabinet.B ?? null;
                const C = cabinet.C ?? null;
                const Path = cabinet.Path ?? null;
                const mass = cabinet.mass ?? null;
                const cabinetName = cabinet.name ?? null; 
                const price = cabinet.price ?? null;
               
                // console.log('Координата A:', A);
                // console.log('Координата B:', B);
                // console.log('Координата C:', C);
                // console.log('Путь к модели:', Path);
                // console.log('Масса:', mass);
                // console.log('Название:', cabinetName);
                // console.log('Цена:', price);

                await loadModel(A,B,C,Path);

                // for (const [key, value] of Object.entries(result[name])) {

                // if (key === 'Path') {
                //     // Теперь код честно остановится и дождется загрузки шкафа
                //     await loadModel(value);
                // }
            // }

            }            
            // console.log('name:', name);
        }

        for (const name in result) {
            if (name === 'elements') {
            
                for (const [key, value] of Object.entries(result[name])) {
                    // console.log('key204:', key);
                    // console.log('value204:', value);
                    const { X, Y, Z, path } = value;
                    // Теперь у вас есть готовые переменные, с которыми можно работать:
                    // console.log('Координата X:', X);       // Выведет: 50.5
                    // console.log('Координата Y:', Y);       // Выведет: 316.5
                    // console.log('Координата Z:', Z);       // Выведет: 0
                    // console.log('Путь к модели:', path);   // Выведет: "automat/Автоматический..." 

                    await add_model(X,Y,Z,path)
                }
            }            
            // console.log('name:', name);
        }
//      console.log(`  checkbox_AVR: ${dataObject.checkbox_AVR}`);  
});


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
    // document.getElementsByClassName('loader-container')[0].style.display = 'flex';
    init();
    // animate();
    // addButton();
}

function init() {
    initScene();
    initCamera();
    initRenderer();    
    initLoaders();
    initControls();
    // loadModel();
    animate();
    document.getElementsByClassName('loader-container')[0].style.display = 'none';


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
    CAMERA = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 0.1, 100);
    CAMERA.position.x = 0;
    CAMERA.position.y = 0;
    CAMERA.position.z = 1;
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

function loadModel(A,B,C,path) {

    GLB_LOADER = new GLTFLoader();
    GLB_LOADER.load(
        `static/models/${path}`,
        function(gltf) {
            const model = gltf.scene;
            model.position.set(-B/2, -A/2, -C/2);
            model.scale.set(1, 1, 1);
            SCENE.add(model);
            console.log('Модель загружена!');
            MAIN_MODEL = model;
            // Добавляем оси к модели
            // addAxesToModel(model, 0.5); // Длина осей — 5 единиц
            // Ищем дверцу и делаем её прозрачной
            model.traverse(child => {

                const type = child.type || 'Unknown';
                const name = child.name || 'Без имени';
                
                // console.log(`Тип: ${type}, Имя: "${name}"`);

                if (child.name === 'mesh_0') {
                    // Включаем прозрачность
                    child.material.transparent = true;
                    // Устанавливаем уровень прозрачности (0 — полностью прозрачно, 1 — непрозрачно)
                    child.material.opacity = 0.3;
                // console.log('Дверца стала прозрачной');
                }
            });
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
    CONTROLS.minDistance = 1;
    CONTROLS.maxDistance = 20;
    // CONTROLS.autoRotate = true;
    CONTROLS.autoRotate = false;
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


// Добавить модель
// function addButton() {
//   const button = document.getElementById('button_add');
//   button.addEventListener('click', add_model);
// }

// Функция добавления модели относительно основной
function add_model(X, Y, Z, path) {     

    const loader = new GLTFLoader();
    loader.load(
    `static/models/${path}`, // Путь к новой модели
    // `static/models/16A.glb`, // Путь к новой модели
    function(gltf) {
        const newModel = gltf.scene;      
        newModel.position.copy(MAIN_MODEL.position);
        // newModel.rotation.x = THREE.MathUtils.degToRad(90);
        newModel.position.x += X;   // смещение по х
        newModel.position.y += Y;
        newModel.position.z += 13.9/1000;
        console.log('X',X);
        console.log('Y',Y);
        console.log('Z',Z);
        // newModel.scale.copy(MAIN_MODEL.scale);
        
        SCENE.add(newModel);
        ADD_MODELS.push(newModel);
        console.log('ADD_MODELS',ADD_MODELS);
    },
    function(xhr) { console.log('Загрузка новой модели: ' + (xhr.loaded / xhr.total * 100) + '%'); },
    function(error) { console.error('Ошибка загрузки новой модели:', error); }
  );
}

/////////////////////////////// Тестовое удаление модели ///////////////////////////////////////////
function clearScene() {
    // Удаляем и очищаем MAIN_MODEL
    if (MAIN_MODEL) {
        SCENE.remove(MAIN_MODEL);
        MAIN_MODEL.traverse(child => {
            if (child.isMesh) {
                child.geometry.dispose();
                if (Array.isArray(child.material)) {
                    child.material.forEach(mat => mat.dispose());
                } else {
                    child.material.dispose();
                }
            }
        });
        MAIN_MODEL = null;
    }

    // Удаляем и очищаем все дополнительные модели
    ADD_MODELS.forEach(model => {
        if (model) {
            SCENE.remove(model);
            model.traverse(child => {
                if (child.isMesh) {
                    child.geometry.dispose();
            if (Array.isArray(child.material)) {
                child.material.forEach(mat => mat.dispose());
            } else {
                child.material.dispose();
            }
        }
    });
        }
    });
    ADD_MODELS = []; // Очищаем массив

    console.log('Сцена очищена');
}