import streamlit as st
from streamlit_p5 import p5

# Streamlit UI 설정
st.title("🍎 현실적인 2D 물리 엔진 시뮬레이션 (Matter.js & p5.js)")
st.markdown("---")
st.subheader("💡 사용 방법")
st.markdown("""
1.  **공 놓기:** 화면 아무 곳이나 **마우스 왼쪽 버튼**을 클릭하면 공이 생성됩니다.
2.  **드래그:** 생성된 공을 **왼쪽 버튼**으로 클릭한 상태로 움직여서 위치를 옮길 수 있습니다.
3.  **중력:** 공을 놓으면 아래로 떨어집니다. (기본 설정)
4.  **충돌:** 공들이 서로 부딪히면 현실처럼 튕겨 나갑니다.
""")
st.markdown("---")

# P5.js 코드를 담을 문자열 변수
# 이 Javascript 코드가 물리 엔진 역할을 합니다.
p5_code = f"""
const {st.session_state.get('num_balls', 5)} = 5; // Streamlit에서 변수 가져오기 (선택 사항)

// Matter.js 모듈 변수
let Engine = Matter.Engine,
    Render = Matter.Render,
    Runner = Matter.Runner,
    Bodies = Matter.Bodies,
    Composite = Matter.Composite,
    MouseConstraint = Matter.MouseConstraint,
    Mouse = Matter.Mouse,
    World = Matter.World;

let engine;
let world;
let boxes = [];
let ground;
let mConstraint; // 마우스 제약 (드래그 기능)

function setup() {{
    // 캔버스 크기 설정 (Streamlit 창에 맞춰서)
    createCanvas(600, 400); 

    // 1. 엔진 생성 및 중력 설정
    engine = Engine.create();
    world = engine.world;
    world.gravity.y = 1; // 중력 활성화 (아래로 떨어짐)

    // 2. 바닥 (벽) 생성 (충돌체)
    // isStatic: 움직이지 않는 벽
    ground = Bodies.rectangle(width / 2, height - 10, width, 20, {{ isStatic: true }});
    World.add(world, ground);
    
    // 3. 마우스 드래그 기능 추가 (MouseConstraint)
    let canvasmouse = Mouse.create(canvas.elt);
    canvasmouse.pixelRatio = pixelDensity(); // 고해상도 처리
    let options = {{
        mouse: canvasmouse
    }}
    // 마우스와 물리 세계를 연결하여 드래그 가능하게 함
    mConstraint = MouseConstraint.create(engine, options);
    World.add(world, mConstraint);

    // 4. 러너 (물리 업데이트) 시작
    Runner.run(Runner.create(), engine);
}}

function mouseClicked() {{
    // 마우스 클릭 시 공 생성 (드래그가 아닌 단순 클릭인 경우에만)
    if (!mConstraint.body) {{
        // Bodies.circle(x, y, radius, [options])
        let newBall = Bodies.circle(mouseX, mouseY, 15, {{
            restitution: 0.8, // 반발력 (탄성)
            friction: 0.001,  // 마찰
            density: 0.01     // 밀도
        }});
        World.add(world, newBall);
    }}
}}

function draw() {{
    background(220); // 배경색

    // 1. 물리 엔진 업데이트 (setup에서 이미 Runner가 처리)
    
    // 2. 모든 객체 그리기
    
    // 바닥 그리기
    fill(100);
    rectMode(CENTER);
    rect(ground.position.x, ground.position.y, width, 20);

    // 공 그리기
    let bodies = Composite.allBodies(world);

    for (let i = 0; i < bodies.length; i++) {{
        let body = bodies[i];
        
        // 정적 오브젝트(바닥)는 그리지 않음
        if (body.isStatic) continue; 

        let pos = body.position;
        let angle = body.angle;
        
        push(); // 현재 변환 상태 저장
        translate(pos.x, pos.y);
        rotate(angle);
        
        fill(255, 0, 100); // 분홍색 공
        ellipse(0, 0, body.circleRadius * 2); // 원 그리기
        
        pop(); // 저장된 변환 상태 복원
    }}
    
    // 마우스 드래그 연결선 그리기 (Matter.js 마우스 제약 시각화)
    if (mConstraint.body) {{
        let pos = mConstraint.body.position;
        let offset = mConstraint.constraint.pointB;
        let m = mConstraint.mouse.position;
        
        stroke(0, 255, 0); // 초록색 선
        line(pos.x + offset.x, pos.y + offset.y, m.x, m.y);
    }}
}}
"""

# P5.js 컴포넌트 호출
# 컴포넌트가 Javascript 코드를 실행하고 그 결과를 Streamlit에 표시합니다.
p5(p5_code, width=600, height=400)
