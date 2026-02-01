## Pygame 기반 발로란트 에임 연습 프로그램 - 설계 문서

### 제안 파일 구조
프로젝트의 기본 구조는 다음과 같이 구성합니다.

```
aim_trainer/
├── main.py                 # 프로그램의 시작점, 메인 루프 실행
├── game_controller.py      # 전체 게임 상태와 화면 전환을 관리
├── settings.py             # 화면 크기, 색상, FPS 등 전역 설정값 관리
│
├── screens/
│   ├── __init__.py
│   ├── base_screen.py      # 모든 화면 클래스가 상속받을 기본 클래스
│   ├── start_screen.py     # 시작 화면 (메인 메뉴)
│   └── game_screen.py      # 게임 플레이 화면
│
└── entities/
    ├── __init__.py
    ├── button.py           # 재사용 가능한 버튼 클래스
    └── target.py           # 타겟(공) 클래스
```

### 개발 우선순위 및 설계 내용

#### **[우선순위 1] 기본 구조 및 인프라 (Foundational Infrastructure)**
가장 먼저 구현되어야 할 핵심 기반입니다. 이 구조가 완성되면 다른 부분들을 안정적으로 개발할 수 있습니다.

1.  **`settings.py`**:
    - **설계**: 게임의 모든 설정값을 변수로 저장합니다. (예: `SCREEN_WIDTH`, `SCREEN_HEIGHT`, `FPS`, `COLORS`, `FONT_NAME`)
    - **역할**: 게임의 주요 속성을 한 곳에서 쉽게 변경하고 관리할 수 있게 합니다.

2.  **`screens/base_screen.py`**:
    - **설계**: 모든 화면(Screen)이 가져야 할 기본 인터페이스를 정의하는 추상 클래스(`BaseScreen`)를 만듭니다.
    - **역할**: `handle_events()`, `update()`, `draw(screen)` 메소드를 포함하여, 모든 화면이 일관된 구조를 갖도록 강제합니다. 이는 화면 전환 로직을 단순하게 만듭니다.

3.  **`entities/button.py`**:
    - **설계**: 화면에 텍스트가 포함된 사각형 버튼을 그리는 `Button` 클래스를 구현합니다.
    - **역할**: 마우스 오버 및 클릭 이벤트를 감지하는 기능을 포함합니다. 시작 화면과 게임 종료 화면에서 재사용됩니다.

4.  **`game_controller.py`**:
    - **설계**: 게임의 메인 루프를 관리하고, 현재 어떤 화면을 보여줄지 결정하는 `GameController` 클래스를 구현합니다. '상태 머신(State Machine)' 패턴을 단순하게 적용합니다.
    - **역할**: 화면 간의 전환(예: `start_screen` -> `game_screen`)을 처리합니다. 각 화면은 자신의 로직에만 집중하고, 화면 전환이 필요할 때 `GameController`에 요청만 하면 됩니다.

5.  **`main.py`**:
    - **설계**: Pygame을 초기화하고, `GameController`의 인스턴스를 생성하여 메인 루프를 실행하는 역할을 합니다. 프로그램의 진입점(Entry Point)입니다.

#### **[우선순위 2] 병렬 개발 화면 (Parallel Development Screens)**
기본 인프라가 구축된 후, 아래 두 화면은 독립적으로 개발을 진행할 수 있습니다.

**Track A: `screens/start_screen.py`**
- **설계**: `BaseScreen`을 상속받는 `StartScreen` 클래스를 구현합니다.
- **책임**:
    - `entities.button`을 사용하여 '시작'과 '종료' 버튼 인스턴스를 생성합니다.
    - `handle_events()`에서 버튼 클릭을 감지합니다.
    - '시작' 버튼이 클릭되면 `GameController`에 게임 화면으로 전환하도록 신호를 보냅니다.
    - `draw()`에서 화면 타이틀과 버튼들을 그립니다.

**Track B: `screens/game_screen.py`**
- **설계**: `BaseScreen`을 상속받는 `GameScreen` 클래스를 구현합니다. 내부적으로 `COUNTDOWN`, `PLAYING`, `GAME_OVER` 상태를 가집니다.
- **책임**:
    - **`entities/target.py` 개발**: `pygame.sprite.Sprite`를 상속받는 `Target` 클래스를 먼저 또는 동시에 개발합니다. `Target`은 자신의 위치, 크기, 점수 값을 가집니다.
    - `GameScreen`은 `Target`들을 관리하기 위해 Pygame의 `sprite.Group`을 사용합니다.
    - `update()` 메소드 내에서 현재 내부 상태(`COUNTDOWN`, `PLAYING` 등)에 따라 타이머 감소, 타겟 생성 및 업데이트 로직을 처리합니다.
    - `handle_events()`에서 마우스 클릭(사격) 이벤트를 처리하고, 타겟 명중 여부를 판별합니다.
    - `draw()`에서 HUD(점수, 시간)와 타겟, 조준선을 그립니다.
    - 게임 종료 시(`GAME_OVER` 상태) 최종 점수와 '다시 시작', '메인으로' 버튼을 화면에 표시합니다.