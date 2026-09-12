import re
import streamlit as st

st.set_page_config(
    page_title="오늘 건네는 한 문장",
    page_icon="🌿",
    layout="centered",
)

st.markdown("""
<style>
.block-container {
    max-width: 760px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}
.result-box {
    padding: 1.45rem 1.3rem;
    border-radius: 16px;
    background: rgba(128,128,128,0.06);
    margin-top: 1.2rem;
    line-height: 1.95;
    font-size: 1.05rem;
}
.quote-card {
    padding: 1.9rem 1.6rem;
    border-radius: 18px;
    border: 1px solid rgba(128,128,128,0.22);
    margin-top: 1.3rem;
}
.quote-title {
    font-size: 1.08rem;
    font-weight: 700;
    margin-bottom: 1rem;
}
.quote-text {
    font-size: 1.48rem;
    line-height: 1.78;
    font-weight: 700;
    margin-bottom: 1rem;
}
.quote-meta {
    font-size: 0.95rem;
    opacity: 0.78;
}
.small-note {
    font-size: 0.88rem;
    opacity: 0.70;
    margin-top: 1rem;
}
</style>
""", unsafe_allow_html=True)

QUOTES = [{'text': '오늘 하루의 빛깔을 바꾸는 것, 그것이 가장 높은 예술이다.', 'author': '헨리 데이비드 소로', 'source': '『Walden』, “Where I Lived, and What I Lived For”', 'type': '산문', 'tags': ['오늘', '관점 전환']}, {'text': '우주는 우리가 바라보는 것보다 더 넓다.', 'author': '헨리 데이비드 소로', 'source': '『Walden』, “Conclusion”', 'type': '산문', 'tags': ['관점 전환', '가능성']}, {'text': '자신을 믿어라. 모든 마음은 그 단단한 줄에 울린다.', 'author': '랠프 월도 에머슨', 'source': '「Self-Reliance」', 'type': '산문', 'tags': ['자기신뢰']}, {'text': '하루하루는 알지 못하는 것을 세월은 많이 가르쳐 준다.', 'author': '랠프 월도 에머슨', 'source': '「Experience」', 'type': '산문', 'tags': ['관점 전환', '위로']}, {'text': '지혜의 변함없는 표지는 평범한 것에서 놀라운 것을 보는 데 있다.', 'author': '랠프 월도 에머슨', 'source': '『Nature』', 'type': '산문', 'tags': ['관점 전환', '오늘']}, {'text': '나는 지금의 나로 존재한다. 그것으로 충분하다.', 'author': '월트 휘트먼', 'source': '「Song of Myself」 20', 'type': '시', 'tags': ['자기신뢰', '위로']}, {'text': '나는 크다. 내 안에는 수많은 모습이 함께 있다.', 'author': '월트 휘트먼', 'source': '「Song of Myself」 51', 'type': '시', 'tags': ['자기이해', '자기신뢰']}, {'text': '이제 나는 행운을 구하지 않는다. 내가 곧 나의 행운이다.', 'author': '월트 휘트먼', 'source': '「Song of the Open Road」', 'type': '시', 'tags': ['자기신뢰', '용기']}, {'text': '나는 지금 보이는 것 말고도 아직 보이지 않는 많은 것이 여기 있다고 믿는다.', 'author': '월트 휘트먼', 'source': '「Song of the Open Road」', 'type': '시', 'tags': ['가능성', '희망']}, {'text': '네가 강과 하늘을 보며 느끼는 것처럼, 나도 그렇게 느꼈다.', 'author': '월트 휘트먼', 'source': '「Crossing Brooklyn Ferry」', 'type': '시', 'tags': ['관계', '위로']}, {'text': '네가 여기 있다는 것. 삶이 계속되고, 너도 그 안에 한 구절을 보탤 수 있다는 것.', 'author': '월트 휘트먼', 'source': '「O Me! O Life!」', 'type': '시', 'tags': ['자기존재', '희망', '자기신뢰']}, {'text': '영원은 수많은 ‘지금’으로 이루어진다.', 'author': '에밀리 디킨슨', 'source': '「Forever—is composed of Nows—」', 'type': '시', 'tags': ['오늘', '관점 전환']}, {'text': '나는 가능성 속에 산다.', 'author': '에밀리 디킨슨', 'source': '「I dwell in Possibility—」', 'type': '시', 'tags': ['가능성', '희망']}, {'text': '우리는 일어서야 할 때가 오기 전까지 자신이 얼마나 높이 오를 수 있는지 모른다.', 'author': '에밀리 디킨슨', 'source': '「We never know how high we are」', 'type': '시', 'tags': ['자기신뢰', '용기', '가능성']}, {'text': '희망은 깃털을 가진 것, 영혼에 내려앉아 노래하는 것.', 'author': '에밀리 디킨슨', 'source': '「“Hope” is the thing with feathers—」', 'type': '시', 'tags': ['희망', '위로']}, {'text': '가장 용감한 사람도 잠시 더듬으며 걷는다.', 'author': '에밀리 디킨슨', 'source': '「We grow accustomed to the Dark」', 'type': '시', 'tags': ['위로', '용기']}, {'text': '새벽이 언제 올지 몰라 나는 모든 문을 열어 둔다.', 'author': '에밀리 디킨슨', 'source': '「Not knowing when the Dawn will come」', 'type': '시', 'tags': ['가능성', '희망']}, {'text': '마음은 하늘보다 넓다.', 'author': '에밀리 디킨슨', 'source': '「The Brain—is wider than the Sky—」', 'type': '시', 'tags': ['자기신뢰', '자기이해']}, {'text': '우리는 세월과 함께 낡아지는 것이 아니라, 날마다 새로워진다.', 'author': '에밀리 디킨슨', 'source': '1874년 편지, 『Letters of Emily Dickinson』', 'type': '서간', 'tags': ['다시 시작', '오늘']}, {'text': '지금은 그 질문들을 살아 보라.', 'author': '라이너 마리아 릴케', 'source': '『Letters to a Young Poet』, Letter 4, 1903.7.16', 'type': '서간', 'tags': ['관점 전환', '오늘', '자기이해']}, {'text': '우리의 의심은 때로, 시도했다면 얻었을 것을 놓치게 한다.', 'author': '윌리엄 셰익스피어', 'source': '『Measure for Measure』 1막 4장', 'type': '희곡', 'tags': ['용기', '가능성']}, {'text': '우리가 찾는 해결책은 종종 우리 자신 안에 있다.', 'author': '윌리엄 셰익스피어', 'source': '『All’s Well That Ends Well』 1막 1장', 'type': '희곡', 'tags': ['자기신뢰', '자기이해']}, {'text': '우리 삶의 실은 좋은 것과 좋지 않은 것이 함께 섞여 짜인다.', 'author': '윌리엄 셰익스피어', 'source': '『All’s Well That Ends Well』 4막 3장', 'type': '희곡', 'tags': ['위로', '관점 전환']}, {'text': '운은 키를 잡지 않은 배도 항구로 데려올 때가 있다.', 'author': '윌리엄 셰익스피어', 'source': '『Cymbeline』 4막 3장', 'type': '희곡', 'tags': ['관점 전환', '희망']}, {'text': '세상에는 우리가 생각해 낸 것보다 더 많은 것이 있다.', 'author': '윌리엄 셰익스피어', 'source': '『Hamlet』 1막 5장', 'type': '희곡', 'tags': ['가능성', '관점 전환']}, {'text': '나는 새가 아니다. 어떤 그물도 나를 가둘 수 없다. 나는 독립된 의지를 가진 자유로운 사람이다.', 'author': '샬럿 브론테', 'source': '『Jane Eyre』 Ch.23', 'type': '소설', 'tags': ['자기신뢰', '용기']}, {'text': '나는 폭풍이 두렵지 않다. 내 배를 다루는 법을 배우고 있으니까.', 'author': '루이자 메이 올컷', 'source': '『Little Women』 Part II, Ch.44', 'type': '소설', 'tags': ['용기', '자기신뢰']}, {'text': '어제로 돌아가도 소용없어. 나는 이미 그때와 다른 사람이니까.', 'author': '루이스 캐럴', 'source': '『Alice’s Adventures in Wonderland』 Ch.10', 'type': '소설', 'tags': ['다시 시작', '오늘']}, {'text': '뒤로만 움직이는 기억이라면 그다지 좋은 기억은 아니지.', 'author': '루이스 캐럴', 'source': '『Through the Looking-Glass』 Ch.5', 'type': '소설', 'tags': ['관점 전환', '다시 시작']}, {'text': '진짜 용기는 두렵지 않은 것이 아니라, 두려운 채로 위험에 맞서는 것이다.', 'author': 'L. 프랭크 바움', 'source': '『The Wonderful Wizard of Oz』 Ch.15', 'type': '소설', 'tags': ['용기', '자기신뢰']}, {'text': '이 순간까지 나는 나 자신을 몰랐다.', 'author': '제인 오스틴', 'source': '『Pride and Prejudice』 Ch.36', 'type': '소설', 'tags': ['자기이해', '관점 전환']}, {'text': '사람의 말 속에 완전한 진실이 그대로 담기는 경우는 아주 드물다.', 'author': '제인 오스틴', 'source': '『Emma』 Ch.49', 'type': '소설', 'tags': ['관점 전환', '관계']}, {'text': '한 가지 일을 여러 관점에서 바라보지 못하는 것은 좁은 생각이다.', 'author': '조지 엘리엇', 'source': '『Middlemarch』 Ch.7', 'type': '소설', 'tags': ['관점 전환']}, {'text': '정의하는 순간, 한계를 긋는다.', 'author': '오스카 와일드', 'source': '『The Picture of Dorian Gray』 Ch.17', 'type': '소설', 'tags': ['자기신뢰', '관점 전환']}, {'text': '사람의 진짜 완성은 무엇을 가졌느냐가 아니라 어떤 사람이냐에 있다.', 'author': '오스카 와일드', 'source': '「The Soul of Man under Socialism」', 'type': '산문', 'tags': ['자기신뢰', '자기이해']}, {'text': '우리는 모두 진흙탕에 있지만, 그중 누군가는 별을 바라본다.', 'author': '오스카 와일드', 'source': '『Lady Windermere’s Fan』 3막', 'type': '희곡', 'tags': ['관점 전환', '희망']}, {'text': '남을 흉내 내 성공하는 것보다 자기 방식으로 실패하는 편이 낫다.', 'author': '허먼 멜빌', 'source': '「Hawthorne and His Mosses」', 'type': '평론', 'tags': ['자기신뢰', '다시 시작']}, {'text': '남의 방식으로 옳기보다 자기 방식으로 틀리는 편이 낫다.', 'author': '표도르 도스토옙스키', 'source': '『Crime and Punishment』 Part III, Ch.1', 'type': '소설', 'tags': ['자기신뢰', '다시 시작']}, {'text': '한 문이 닫히면 다른 문이 열린다.', 'author': '미겔 데 세르반테스', 'source': '『Don Quixote』 Part I, Ch.21', 'type': '소설', 'tags': ['다시 시작', '희망']}, {'text': '희망을 품고 가는 것은 도착하는 것보다 더 나은 일일 때가 있다.', 'author': '로버트 루이스 스티븐슨', 'source': '「El Dorado」', 'type': '산문', 'tags': ['관점 전환', '희망']}, {'text': '겉모습으로 판단하지 말고, 근거를 보라.', 'author': '찰스 디킨스', 'source': '『Great Expectations』 Ch.40', 'type': '소설', 'tags': ['관점 전환']}, {'text': '명백해 보이는 사실만큼 우리를 속이기 쉬운 것도 없다.', 'author': '아서 코난 도일', 'source': '「The Boscombe Valley Mystery」', 'type': '소설', 'tags': ['관점 전환']}, {'text': '자료를 갖기 전에 이론을 세우는 것은 큰 실수다.', 'author': '아서 코난 도일', 'source': '「A Scandal in Bohemia」', 'type': '소설', 'tags': ['관점 전환']}, {'text': '크고 갑작스러운 변화만큼 사람의 마음을 아프게 하는 것도 없다.', 'author': '메리 셸리', 'source': '『Frankenstein』 1818년판, Vol. III, Ch.6', 'type': '소설', 'tags': ['위로', '관점 전환']}, {'text': '삶은 사람들 앞에서 바이올린 독주를 하면서, 연주하는 법을 동시에 배우는 것과 같다.', 'author': '새뮤얼 버틀러', 'source': '「How to Make the Best of Life」', 'type': '산문', 'tags': ['위로', '자기이해']}, {'text': '시간의 좋은 점은 미리 낭비해 버릴 수 없다는 것이다.', 'author': '아널드 베넷', 'source': '『How to Live on 24 Hours a Day』', 'type': '산문', 'tags': ['다시 시작', '오늘']}, {'text': '서두를 필요도, 빛나 보일 필요도, 자기 아닌 다른 사람이 될 필요도 없다.', 'author': '버지니아 울프', 'source': '『A Room of One’s Own』 Ch.1', 'type': '산문', 'tags': ['위로', '자기신뢰']}, {'text': '모험이란, 다르게 바라본 불편함일 뿐이다.', 'author': 'G. K. 체스터턴', 'source': '『All Things Considered』, 「On Running After One’s Hat」', 'type': '산문', 'tags': ['관점 전환', '용기']}, {'text': '어떤 사람은 있는 것을 보며 ‘왜?’라고 묻고, 나는 없던 것을 꿈꾸며 ‘왜 안 돼?’라고 묻는다.', 'author': '조지 버나드 쇼', 'source': '『Back to Methuselah』', 'type': '희곡', 'tags': ['가능성', '용기']}, {'text': '코앞에 있는 것을 제대로 보는 데에도 끊임없는 노력이 필요하다.', 'author': '조지 오웰', 'source': '「In Front of Your Nose」, 1946', 'type': '산문', 'tags': ['관점 전환', '오늘']}, {'text': '절뚝이며 가더라도 뒤로 가는 것은 아니다.', 'author': '칼릴 지브란', 'source': '『The Prophet』, “Good and Evil”', 'type': '산문시', 'tags': ['다시 시작', '위로']}, {'text': '‘진리를 찾았다’고 말하지 말고, ‘하나의 진리를 찾았다’고 말하라.', 'author': '칼릴 지브란', 'source': '『The Prophet』, “Self-Knowledge”', 'type': '산문시', 'tags': ['관점 전환', '자기이해']}, {'text': '오래된 길이 사라진 곳에서 새로운 땅이 경이로움과 함께 모습을 드러낸다.', 'author': '라빈드라나트 타고르', 'source': '『Gitanjali』 37', 'type': '시', 'tags': ['가능성', '다시 시작']}, {'text': '우리는 세상을 잘못 읽고는 세상이 우리를 속였다고 말한다.', 'author': '라빈드라나트 타고르', 'source': '『Stray Birds』 75', 'type': '산문시', 'tags': ['관점 전환']}, {'text': '어떤 일에 대해 꼭 지금 의견을 가져야 하는 것은 아니다.', 'author': '마르쿠스 아우렐리우스', 'source': '『Meditations』 VI.52', 'type': '철학', 'tags': ['관점 전환', '위로']}, {'text': '어떤 것은 우리에게 달려 있고, 어떤 것은 그렇지 않다.', 'author': '에픽테토스', 'source': '『Enchiridion』 §1', 'type': '철학', 'tags': ['관점 전환', '위로']}, {'text': '우리는 현실보다 상상 속에서 더 자주 괴로워한다.', 'author': '세네카', 'source': '『Moral Letters to Lucilius』 Letter 13', 'type': '서간·철학', 'tags': ['관점 전환', '위로']}, {'text': '제비 한 마리가 여름을 만들지 않듯, 하루가 한 사람의 삶 전체를 결정하지 않는다.', 'author': '아리스토텔레스', 'source': '『Nicomachean Ethics』 I.7', 'type': '철학', 'tags': ['위로', '관점 전환']}, {'text': '우리는 해보면서 배운다.', 'author': '아리스토텔레스', 'source': '『Nicomachean Ethics』 II.1', 'type': '철학', 'tags': ['다시 시작', '용기']}, {'text': '세상에서 가장 큰 일은 자기 자신에게 속할 줄 아는 것이다.', 'author': '미셸 드 몽테뉴', 'source': '『Essays』 I, 「Of Solitude」', 'type': '철학', 'tags': ['자기신뢰', '자기이해']}, {'text': '나는 고정된 존재를 그리지 않는다. 변화해 가는 모습을 그린다.', 'author': '미셸 드 몽테뉴', 'source': '『Essays』 III.2, 「Of Repentance」', 'type': '철학', 'tags': ['자기이해', '다시 시작']}, {'text': '확신에서 시작하면 의심으로 끝나고, 의심에서 시작하면 확신에 이를 수 있다.', 'author': '프랜시스 베이컨', 'source': '『The Advancement of Learning』', 'type': '철학', 'tags': ['관점 전환']}, {'text': '진실은 혼란보다 오류를 통해 더 빨리 모습을 드러내기도 한다.', 'author': '프랜시스 베이컨', 'source': '『Novum Organum』 관련 구절', 'type': '철학', 'tags': ['관점 전환', '다시 시작']}, {'text': '다른 사람을 아는 것은 지혜이고, 자기 자신을 아는 것은 밝은 앎이다.', 'author': '노자', 'source': '『도덕경』 33장', 'type': '철학', 'tags': ['자기이해', '자기신뢰']}, {'text': '회오리바람도 아침 내내 불지는 않고, 소나기도 하루 종일 내리지는 않는다.', 'author': '노자', 'source': '『도덕경』 23장', 'type': '철학', 'tags': ['위로', '희망']}, {'text': '아는 것을 안다고 하고, 모르는 것을 모른다고 하는 것. 그것이 아는 것이다.', 'author': '공자', 'source': '『논어』 「위정」 2.17', 'type': '철학', 'tags': ['자기신뢰', '자기이해']}, {'text': '나는 모르는 것을 안다고 생각하지 않는다.', 'author': '플라톤', 'source': '『Apology』 21d, 소크라테스의 말', 'type': '철학', 'tags': ['자기이해', '관점 전환']}, {'text': '지혜로운 사람은 근거에 맞추어 믿음의 정도를 정한다.', 'author': '데이비드 흄', 'source': '『An Enquiry Concerning Human Understanding』 §10', 'type': '철학', 'tags': ['관점 전환']}, {'text': '철학자가 되어라. 그러나 철학 속에서도 여전히 한 사람으로 있어라.', 'author': '데이비드 흄', 'source': '『An Enquiry Concerning Human Understanding』 §1', 'type': '철학', 'tags': ['자기신뢰', '자기이해']}, {'text': '자기 쪽 이야기만 아는 사람은 그것조차 충분히 알지 못한다.', 'author': '존 스튜어트 밀', 'source': '『On Liberty』 Ch.2', 'type': '철학', 'tags': ['관점 전환']}, {'text': '모든 것을 의심하는 것과 모든 것을 믿는 것은 똑같이 편한 방법이다. 둘 다 생각할 필요를 없애기 때문이다.', 'author': '앙리 푸앵카레', 'source': '『Science and Hypothesis』, Preface', 'type': '과학·철학', 'tags': ['관점 전환']}, {'text': '지혜의 기술은 무엇을 지나쳐도 되는지 아는 기술이다.', 'author': '윌리엄 제임스', 'source': '『The Principles of Psychology』 Vol. II, Ch.22', 'type': '심리학', 'tags': ['관점 전환', '위로']}, {'text': '마음에는 이성이 알지 못하는 나름의 이유가 있다.', 'author': '블레즈 파스칼', 'source': '『Pensées』', 'type': '철학', 'tags': ['자기이해', '위로']}, {'text': '우리는 남이 준 이유보다 스스로 발견한 이유에 더 잘 설득된다.', 'author': '블레즈 파스칼', 'source': '『Pensées』', 'type': '철학', 'tags': ['자기신뢰', '자기이해']}, {'text': '불확실함과 의문 속에 있으면서도 성급하게 답을 붙잡지 않을 수 있다.', 'author': '존 키츠', 'source': '조지·톰 키츠에게 보낸 편지, 1817.12.21, “Negative Capability”', 'type': '서간', 'tags': ['관점 전환', '위로']}, {'text': '의심은 편안한 상태가 아니지만, 확신만 하는 것은 어리석은 상태다.', 'author': '볼테르', 'source': '프리드리히 빌헬름에게 보낸 편지, 1770.11.28', 'type': '서간', 'tags': ['관점 전환']}, {'text': '가장 좋은 것을 고집하다 보면 좋은 것마저 놓칠 수 있다.', 'author': '볼테르', 'source': '「La Bégueule」, 1772', 'type': '시·경구', 'tags': ['관점 전환', '위로']}, {'text': '태양은 날마다 새롭다.', 'author': '헤라클레이토스', 'source': 'Fragment DK B6', 'type': '철학', 'tags': ['오늘', '다시 시작']}, {'text': '사람의 행동을 비웃거나 미워하기보다 이해하려고 했다.', 'author': '바뤼흐 스피노자', 'source': '『Tractatus Politicus』 I.4', 'type': '철학', 'tags': ['관점 전환', '관계']}, {'text': '마음은 채워야 할 그릇이라기보다 불붙여야 할 불과 같다.', 'author': '플루타르코스', 'source': '『On Listening』 48C', 'type': '철학', 'tags': ['가능성', '자기신뢰']}, {'text': '큰 사람은 어린아이의 마음을 잃지 않은 사람이다.', 'author': '맹자', 'source': '『맹자』 「이루 하」 12', 'type': '철학', 'tags': ['자기이해', '자기신뢰']}, {'text': '지금 증명된 것도 한때는 오직 상상 속에 있었다.', 'author': '윌리엄 블레이크', 'source': '『The Marriage of Heaven and Hell』', 'type': '시·산문', 'tags': ['가능성', '희망']}, {'text': '기쁨과 슬픔은 촘촘히 함께 짜여 있다.', 'author': '윌리엄 블레이크', 'source': '「Auguries of Innocence」', 'type': '시', 'tags': ['위로', '관점 전환']}, {'text': '겨울이 온다면, 봄이 어찌 멀리 있겠는가.', 'author': '퍼시 비시 셸리', 'source': '「Ode to the West Wind」', 'type': '시', 'tags': ['희망', '위로']}, {'text': '많은 것을 잃었어도, 아직 많은 것이 남아 있다.', 'author': '앨프리드 테니슨', 'source': '「Ulysses」', 'type': '시', 'tags': ['위로', '희망']}, {'text': '살아 있는 지금 속에서 행동하라.', 'author': '헨리 워즈워스 롱펠로', 'source': '「A Psalm of Life」', 'type': '시', 'tags': ['오늘', '용기']}, {'text': '용기는 두려움에 저항하고 그것을 다스리는 것이지, 두려움이 없는 것이 아니다.', 'author': '마크 트웨인', 'source': '『Pudd’nhead Wilson』 Ch.12', 'type': '소설', 'tags': ['용기', '자기신뢰']}, {'text': '가능한 모든 반론을 먼저 해결해야 한다면, 아무것도 시작되지 않을 것이다.', 'author': '새뮤얼 존슨', 'source': '『The History of Rasselas』', 'type': '소설·철학', 'tags': ['용기', '가능성']}, {'text': '일상의 작은 것들에 진짜 관심을 갖는 데에도 삶의 기쁨이 있다.', 'author': '윌리엄 모리스', 'source': '「The Aims of Art」 관련 산문', 'type': '산문', 'tags': ['오늘', '관점 전환']}, {'text': '아무것도 놓치지 않는 사람 가운데 한 사람이 되어 보라.', 'author': '헨리 제임스', 'source': '「The Art of Fiction」', 'type': '평론', 'tags': ['관점 전환', '오늘']}, {'text': '사실이 반대한다는 것이 드러나면, 아무리 아끼던 생각이라도 내려놓을 준비를 해 왔다.', 'author': '찰스 다윈', 'source': '『Autobiography』', 'type': '과학자 기록', 'tags': ['관점 전환', '용기']}, {'text': '자신이 모른다는 것을 분명히 아는 것이 모든 진정한 과학적 진보의 출발이다.', 'author': '제임스 클러크 맥스웰', 'source': 'R. B. 리치필드에게 보낸 편지, 1858.2.5', 'type': '과학자 서간', 'tags': ['자기신뢰', '관점 전환']}, {'text': '새로운 생각은 새롭다는 이유만으로 의심받고 반대받곤 한다.', 'author': '존 로크', 'source': '『An Essay Concerning Human Understanding』, “Epistle to the Reader”', 'type': '철학', 'tags': ['자기신뢰', '가능성']}, {'text': '사람은 자기 시야의 한계를 세상의 한계라고 생각하기 쉽다.', 'author': '아르투어 쇼펜하우어', 'source': '『Parerga and Paralipomena』', 'type': '철학', 'tags': ['관점 전환', '가능성']}, {'text': '행복은 찾아 나섰을 때보다 뜻밖에 찾아올 때가 있다.', 'author': '너새니얼 호손', 'source': '『American Note-Books』, 1851.11.3', 'type': '일기', 'tags': ['관점 전환', '희망']}, {'text': '경험의 결과만이 아니라 경험 그 자체에도 의미가 있다.', 'author': '월터 페이터', 'source': '『The Renaissance』, “Conclusion”', 'type': '평론', 'tags': ['관점 전환', '위로']}, {'text': '서로 다른 것들에서 가장 아름다운 조화가 생긴다.', 'author': '헤라클레이토스', 'source': 'Fragment DK B8', 'type': '철학', 'tags': ['위로', '관점 전환']}, {'text': '삶에는 우리에게 내어 줄 아름다움이 있다.', 'author': '세라 티즈데일', 'source': '「Barter」', 'type': '시', 'tags': ['오늘', '희망']}, {'text': '나의 길은 언제나 새로운 길.', 'author': '윤동주', 'source': '「새로운 길」, 1938.5.10', 'type': '시', 'tags': ['오늘', '다시 시작']}, {'text': '삶은 놀라움의 연속이다.', 'author': '랠프 월도 에머슨', 'source': '「Experience」', 'type': '산문', 'tags': ['가능성', '오늘']}]

# ------------------------------------------------------------
# 1) 기분: 감정의 방향을 먼저 결정
# ------------------------------------------------------------
MOOD_RULES = {
    "기쁨": ["행복", "좋아", "기분 좋", "즐거", "신나", "설레", "뿌듯", "편안", "평온"],
    "분노": ["짜증", "화나", "화가", "분노", "열받", "억울", "빡쳐"],
    "불안": ["불안", "걱정", "긴장", "초조", "두렵", "무섭", "떨려"],
    "슬픔": ["슬프", "속상", "우울", "서럽", "눈물", "상처"],
    "피로": ["피곤", "지쳐", "졸려", "기운 없", "무기력", "힘들"],
    "혼란": ["답답", "막막", "모르겠", "혼란", "복잡", "갈피"],
    "중립": ["그냥", "보통", "괜찮", "무난"],
}

# ------------------------------------------------------------
# 2) 이유: 상황을 별도로 판단
# ------------------------------------------------------------
CONTEXT_RULES = {
    "관계갈등": [
        "친구와 싸", "친구랑 싸", "다퉜", "서운", "배신", "의리", "신뢰를 지키지",
        "동료", "관계가 안 좋", "어색", "말다툼", "화해"
    ],
    "관계긍정": [
        "친구와 즐", "친구랑 즐", "함께 있어서", "같이 있어서", "좋은 사람",
        "친구를 만나", "가족과 함께", "대화가 잘"
    ],
    "혼자휴식": [
        "혼자만의 시간", "혼자 있는 시간", "혼자 있어서 좋", "혼자라서 좋",
        "혼자 쉬", "혼자 보내", "조용히 쉬", "내 시간을 즐"
    ],
    "외로움": [
        "혼자라서 외롭", "혼자여서 외롭", "외롭", "아무도 없", "소외", "고립"
    ],
    "비교": [
        "사람들보다", "남들보다", "다른 사람보다", "친구보다", "비교",
        "뒤처", "뒤쳐", "못 따라", "속도가 느", "나만 느"
    ],
    "학업": [
        "시험", "성적", "공부", "수능", "입시", "대학", "과제", "수업",
        "문제 풀이", "코딩", "바이브 코딩", "발표", "면접"
    ],
    "실수실패": [
        "실수", "실패", "틀렸", "망했", "잘 안돼", "안 풀", "후회", "포기"
    ],
    "성취": [
        "잘했", "성공", "끝냈", "해냈", "칭찬", "성과", "좋은 결과", "완성"
    ],
    "피로휴식": [
        "잠을 못", "잠 부족", "늦게 자", "과로", "피곤해서", "몸이 안 좋", "아파서"
    ],
    "기대": [
        "기대돼", "기다리던", "좋은 일이", "여행", "약속", "만나기로", "행사"
    ],
    "불확실": [
        "결과를 몰라", "어떻게 될지", "모르겠", "결정 못", "앞으로가", "막막"
    ],
}

# ------------------------------------------------------------
# 3) 바람: 추천 방향을 최종 결정
# ------------------------------------------------------------
WISH_RULES = {
    "위로": ["편해졌", "편안해", "마음이 가벼", "덜 힘들", "쉬고 싶", "괜찮아지고"],
    "자기신뢰": ["나를 믿", "자신감", "잘하고 싶", "내가 할 수", "스스로 믿"],
    "재도전": ["다시 해", "다시 시작", "포기하지", "재도전", "한번 더"],
    "관계회복": ["화해", "친해지고", "관계가 좋아", "잘 지내고", "오해가 풀"],
    "휴식유지": ["쉬고 싶", "푹 쉬", "이 시간을 즐", "계속 편안", "여유롭"],
    "긍정유지": ["계속 행복", "좋은 기분", "이 기분 유지", "즐겁게", "행복했으면"],
    "집중": ["집중하고", "오늘 잘 보내", "차분히", "해야 할 일"],
    "가능성": ["가능성을", "희망", "잘됐으면", "좋은 결과", "앞으로 잘"],
    "이해": ["정리됐으면", "이해하고", "생각이 정리", "알고 싶"],
}

MOOD_TO_TAGS = {
    "기쁨": ["오늘", "희망"],
    "분노": ["관점 전환", "자기이해"],
    "불안": ["위로", "관점 전환", "자기신뢰"],
    "슬픔": ["위로", "희망"],
    "피로": ["위로", "오늘"],
    "혼란": ["관점 전환", "자기이해", "가능성"],
    "중립": ["오늘", "관점 전환"],
}

CONTEXT_TO_TAGS = {
    "관계갈등": ["관계", "위로", "관점 전환"],
    "관계긍정": ["관계", "오늘", "희망"],
    "혼자휴식": ["자기이해", "자기신뢰", "오늘"],
    "외로움": ["관계", "위로", "자기존재"],
    "비교": ["자기신뢰", "위로", "관점 전환"],
    "학업": ["자기신뢰", "오늘", "관점 전환"],
    "실수실패": ["다시 시작", "자기신뢰", "위로"],
    "성취": ["자기신뢰", "희망", "오늘"],
    "피로휴식": ["위로", "오늘"],
    "기대": ["희망", "가능성", "오늘"],
    "불확실": ["관점 전환", "가능성", "위로"],
}

WISH_TO_TAGS = {
    "위로": ["위로"],
    "자기신뢰": ["자기신뢰"],
    "재도전": ["다시 시작", "용기"],
    "관계회복": ["관계", "위로"],
    "휴식유지": ["위로", "오늘"],
    "긍정유지": ["오늘", "희망"],
    "집중": ["오늘"],
    "가능성": ["가능성", "희망"],
    "이해": ["관점 전환", "자기이해"],
}

SPECIAL_QUOTE_RULES = [
    {
        "mood": None,
        "context": "비교",
        "wish": None,
        "preferred": [
            "서두를 필요도, 빛나 보일 필요도, 자기 아닌 다른 사람이 될 필요도 없다.",
            "절뚝이며 가더라도 뒤로 가는 것은 아니다.",
            "나는 지금의 나로 존재한다. 그것으로 충분하다.",
            "남을 흉내 내 성공하는 것보다 자기 방식으로 실패하는 편이 낫다."
        ]
    },
    {
        "mood": "기쁨",
        "context": "혼자휴식",
        "wish": None,
        "preferred": [
            "세상에서 가장 큰 일은 자기 자신에게 속할 줄 아는 것이다.",
            "나는 지금의 나로 존재한다. 그것으로 충분하다.",
            "일상의 작은 것들에 진짜 관심을 갖는 데에도 삶의 기쁨이 있다.",
            "삶에는 우리에게 내어 줄 아름다움이 있다."
        ]
    },
    {
        "mood": "분노",
        "context": "관계갈등",
        "wish": None,
        "preferred": [
            "사람의 행동을 비웃거나 미워하기보다 이해하려고 했다.",
            "사람의 말 속에 완전한 진실이 그대로 담기는 경우는 아주 드물다.",
            "한 가지 일을 여러 관점에서 바라보지 못하는 것은 좁은 생각이다."
        ]
    },
    {
        "mood": "불안",
        "context": None,
        "wish": None,
        "preferred": [
            "우리는 현실보다 상상 속에서 더 자주 괴로워한다.",
            "어떤 것은 우리에게 달려 있고, 어떤 것은 그렇지 않다.",
            "가장 용감한 사람도 잠시 더듬으며 걷는다."
        ]
    },
    {
        "mood": None,
        "context": "실수실패",
        "wish": "재도전",
        "preferred": [
            "우리는 해보면서 배운다.",
            "절뚝이며 가더라도 뒤로 가는 것은 아니다.",
            "태양은 날마다 새롭다."
        ]
    },
]

def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip().lower())

def detect_label(text: str, rules: dict, default=None):
    t = normalize(text)
    best_label = default
    best_hits = 0
    for label, keywords in rules.items():
        hits = sum(1 for k in keywords if k in t)
        if hits > best_hits:
            best_hits = hits
            best_label = label
    return best_label

def detect_mood(text: str):
    return detect_label(text, MOOD_RULES, "중립")

def detect_context(text: str):
    t = normalize(text)

    # 문맥 충돌 방지: '혼자'라는 단어만으로 외로움으로 가지 않음
    if any(k in t for k in ["혼자만의 시간", "혼자 있는 시간", "혼자 있어서 좋", "혼자라서 좋", "혼자 쉬", "내 시간을 즐"]):
        return "혼자휴식"

    if any(k in t for k in ["혼자라서 외롭", "혼자여서 외롭", "외롭", "소외", "고립"]):
        return "외로움"

    return detect_label(text, CONTEXT_RULES, None)

def detect_wish(text: str):
    return detect_label(text, WISH_RULES, None)

def special_bonus(quote, mood_label, context_label, wish_label):
    bonus = 0
    for rule in SPECIAL_QUOTE_RULES:
        if rule["mood"] is not None and rule["mood"] != mood_label:
            continue
        if rule["context"] is not None and rule["context"] != context_label:
            continue
        if rule["wish"] is not None and rule["wish"] != wish_label:
            continue
        if quote["text"] in rule["preferred"]:
            rank = rule["preferred"].index(quote["text"])
            bonus += 35 - rank * 4
    return bonus

def quote_score(quote, mood_label, context_label, wish_label):
    tags = quote["tags"]
    score = 0

    if wish_label:
        for tag in WISH_TO_TAGS[wish_label]:
            if tag in tags:
                score += 16

    if context_label:
        for tag in CONTEXT_TO_TAGS[context_label]:
            if tag in tags:
                score += 9

    if mood_label:
        for tag in MOOD_TO_TAGS[mood_label]:
            if tag in tags:
                score += 5

    score += special_bonus(quote, mood_label, context_label, wish_label)

    # 긍정 감정인데 위로 전용 느낌만 강한 문장은 약간 감점
    if mood_label == "기쁨" and "위로" in tags and "희망" not in tags and "오늘" not in tags:
        score -= 8

    # 분노/관계갈등인데 지나치게 낙관적인 가능성 문장만 있는 경우 감점
    if mood_label == "분노" and context_label == "관계갈등":
        if "관계" not in tags and "관점 전환" not in tags and "자기이해" not in tags:
            score -= 10

    return score

def choose_quote(mood_text: str, reason_text: str, wish_text: str):
    mood_label = detect_mood(mood_text)
    context_label = detect_context(reason_text)
    wish_label = detect_wish(wish_text)

    scored = [
        (quote_score(q, mood_label, context_label, wish_label), idx)
        for idx, q in enumerate(QUOTES)
    ]
    scored.sort(key=lambda x: (-x[0], x[1]))
    return scored[0][1], mood_label, context_label, wish_label

def vocative_name(name: str) -> str:
    clean = name.strip()
    if not clean:
        return ""
    last = clean[-1]
    if "가" <= last <= "힣":
        jong = (ord(last) - ord("가")) % 28
        return clean + ("아" if jong else "야")
    return clean + "아"

def build_support_message(mood_label, context_label, wish_label, quote):
    # 긍정 감정은 '위로'가 아니라 인정·확장
    if mood_label == "기쁨":
        if context_label == "혼자휴식":
            comfort = "혼자 있는 시간이 꼭 외로운 시간인 것은 아니지. 누구의 속도에도 맞출 필요 없이 네가 좋아하는 방식으로 시간을 보내고 있다는 게 지금의 좋은 마음과 잘 이어지는 것 같아."
            reason = "자기 자신에게 온전히 머무는 시간의 의미를 담고 있어서"
        elif context_label == "성취":
            comfort = "무언가를 해냈을 때 느끼는 좋은 마음은 충분히 누려도 좋아. 네가 들인 시간과 노력도 함께 기억해 두면 좋겠어."
            reason = "지금의 성취와 좋은 마음을 오래 기억하게 해 주는 뜻이 담겨 있어서"
        else:
            comfort = "좋은 마음이 드는 순간은 이유를 분석하기보다 충분히 누려도 좋아. 오늘의 기분이 하루를 조금 더 가볍게 만들어 주면 좋겠다."
            reason = "지금의 좋은 마음을 오래 간직하는 데 어울리는 뜻이 담겨 있어서"
        return comfort, reason

    if mood_label == "분노":
        if context_label == "관계갈등":
            comfort = "믿었던 사람에게 서운함이나 화가 생기면 감정이 크게 흔들릴 수 있어. 지금 당장 이해하거나 용서하려고 서두르지 않아도 괜찮아."
            reason = "상대와 상황을 조금 떨어져 바라보는 데 도움이 될 수 있어서"
        else:
            comfort = "화가 난 마음에는 그만한 이유가 있을 수 있어. 감정을 억지로 없애기보다 왜 그런 마음이 들었는지 천천히 살펴봐도 괜찮아."
            reason = "감정에 휩쓸리지 않고 한 번 다른 각도에서 바라보게 해 줄 수 있어서"
        return comfort, reason

    if mood_label == "불안":
        comfort = "아직 정해지지 않은 일은 마음을 쉽게 지치게 해. 지금 당장 모든 답을 정하지 않아도 괜찮아."
        reason = "불안한 순간에도 마음을 조금 넓게 바라볼 수 있게 해 주는 뜻이 담겨 있어서"
        return comfort, reason

    if mood_label == "슬픔":
        comfort = "속상하거나 슬픈 마음은 빨리 정리하려고 할수록 더 무겁게 느껴질 때가 있어. 오늘은 그 마음이 있다는 사실만 인정해도 괜찮아."
        reason = "지금의 마음이 오래 그대로일 필요는 없다는 뜻을 전해 주고 싶어서"
        return comfort, reason

    if mood_label == "피로":
        if context_label == "비교":
            comfort = "처음 해보는 일에서 다른 사람보다 느리다고 느끼는 건 자연스러운 일이야. 중요한 건 남의 속도가 아니라 네가 계속 해보고 있다는 사실이야."
            reason = "남과 비교하기보다 자기 속도로 가도 괜찮다는 뜻이 담겨 있어서"
        else:
            comfort = "피곤한 날에는 평소처럼 해내는 것만으로도 충분히 애쓰고 있는 거야. 잠시 속도를 늦춰도 괜찮아."
            reason = "오늘 하루를 너무 몰아붙이지 않아도 된다는 뜻이 담겨 있어서"
        return comfort, reason

    if mood_label == "혼란":
        comfort = "지금 답이 바로 보이지 않는다고 해서 길이 없는 것은 아니야. 생각이 정리되는 데는 시간이 필요할 때도 있어."
        reason = "지금 보이는 것만으로 가능성을 다 정하지 않아도 된다는 뜻이 담겨 있어서"
        return comfort, reason

    # 중립 또는 분류가 약한 경우
    if context_label == "비교":
        comfort = "다른 사람과 비교하면 내 속도가 더 느리게 느껴질 수 있어. 하지만 배우는 속도와 방식은 사람마다 다를 수 있어."
        reason = "남의 속도보다 자기 방식으로 계속 가는 일이 중요하다는 뜻이 담겨 있어서"
    elif context_label == "관계갈등":
        comfort = "사람 사이의 일은 한쪽 마음만으로 정리되지 않을 때가 많아. 네 마음을 너무 급하게 결론 내리지 않아도 괜찮아."
        reason = "관계를 조금 다른 시선에서 바라보는 데 도움이 될 수 있어서"
    else:
        comfort = "지금 느끼는 마음을 이렇게 적어 본 것만으로도 네 상태를 한 번 돌아본 셈이야."
        reason = "오늘의 마음을 조금 다른 시선으로 바라보는 데 도움이 될 것 같아서"

    return comfort, reason


# ------------------------------------------------------------
# 화면 전환 상태
# ------------------------------------------------------------
if "page" not in st.session_state:
    st.session_state.page = "input"

if st.session_state.page == "input":
    st.title("오늘 건네는 한 문장 🌿")
    st.write("네 가지 질문에 짧게 답하면, 오늘의 마음에 어울리는 문장 하나를 골라 줄게.")

    with st.form("morning_checkin"):
        name = st.text_input(
            "1. 저는 (      )입니다. 이름을 써줘.",
            placeholder="예: 민준",
        )

        mood = st.text_area(
            "2. 지금 기분은 어떠니?",
            placeholder="예: 조금 불안해 / 행복해 / 짜증이 나 / 많이 피곤해",
            height=90,
        )

        reason = st.text_area(
            "3. 왜 그런 것 같아?",
            placeholder="예: 오늘 시험 결과가 나와서 / 혼자만의 시간을 즐기고 있어서",
            height=100,
        )

        wish = st.text_area(
            "4. 바라는 것이 있어?",
            placeholder="예: 마음이 편해졌으면 좋겠어 / 이 좋은 기분이 계속됐으면 좋겠어",
            height=100,
        )

        submitted = st.form_submit_button(
            "오늘의 문장 받기",
            type="primary",
            use_container_width=True,
        )

    if submitted:
        if not all([name.strip(), mood.strip(), reason.strip(), wish.strip()]):
            st.warning("네 가지 질문에 모두 답해 줘.")
        else:
            chosen_idx, mood_label, context_label, wish_label = choose_quote(
                mood, reason, wish
            )

            st.session_state.result = {
                "name": name.strip(),
                "mood": mood.strip(),
                "reason": reason.strip(),
                "wish": wish.strip(),
                "chosen_idx": chosen_idx,
                "mood_label": mood_label,
                "context_label": context_label,
                "wish_label": wish_label,
            }
            st.session_state.page = "result"
            st.rerun()

else:
    result = st.session_state.result
    q = QUOTES[result["chosen_idx"]]
    call_name = vocative_name(result["name"])
    comfort, reason_for_quote = build_support_message(
        result["mood_label"],
        result["context_label"],
        result["wish_label"],
        q,
    )

    st.title("오늘의 문장 🌿")

    st.markdown(
        f"""
        <div class="result-box">
            <strong>{call_name}.</strong><br><br>
            지금은 <strong>‘{result['mood']}’</strong>라고 느끼고 있구나.<br>
            <strong>‘{result['reason']}’</strong>라는 이유도 함께 들려주었네.<br><br>
            {comfort}<br><br>
            그래서 오늘은 <strong>{reason_for_quote}</strong> 이 문장을 골랐어.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <div class="quote-card">
            <div class="quote-title">{result['name']}에게 오늘 건네는 한 문장</div>
            <div class="quote-text">“{q['text']}”</div>
            <div class="quote-meta">— {q['author']}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="small-note">입력한 내용은 별도로 저장하지 않습니다.</div>',
        unsafe_allow_html=True,
    )

    if st.button("처음으로 돌아가기", use_container_width=True):
        st.session_state.page = "input"
        if "result" in st.session_state:
            del st.session_state.result
        st.rerun()
