(()=>{
const reduce=matchMedia('(prefers-reduced-motion: reduce)').matches;
const b=document.querySelector('.menu-btn'),n=document.getElementById('nav');
const setOpen=o=>{n.classList.toggle('open',o);b.setAttribute('aria-expanded',String(o));b.setAttribute('aria-label',o?'Close menu':'Open menu')};
b.addEventListener('click',()=>setOpen(!n.classList.contains('open')));
document.addEventListener('keydown',e=>{if(e.key==='Escape'&&n.classList.contains('open')){setOpen(false);b.focus()}});
n.addEventListener('click',e=>{if(e.target.closest('a'))setOpen(false)});
/* Scroll reveal: progressive enhancement. The js-ready class is added only after setup succeeds,
   so content is always visible if this script fails, is blocked, or motion is reduced. */
if(!reduce&&'IntersectionObserver' in window){
 const els=[...document.querySelectorAll('.sec-h,.col,.rows>div,.split>*,.tbl-wrap,.steps li,.disclaimer,.form-wrap,.cta .wrap>*')];
 els.forEach(el=>{el.classList.add('reveal');el.style.transitionDelay=Math.min([...el.parentNode.children].indexOf(el),4)*70+'ms';if(el.getBoundingClientRect().top<innerHeight*.92)el.classList.add('in')});
 document.documentElement.classList.add('js-ready');
 const io=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}}),{threshold:.12,rootMargin:'0px 0px -6% 0px'});
 els.forEach(el=>{if(!el.classList.contains('in'))io.observe(el)});
}
const today=new Date().toISOString().slice(0,10);
document.querySelectorAll('input[type=date]').forEach(i=>i.min=today);
const q=new URLSearchParams(location.search),topic=document.querySelector('select[name=topic]');
if(topic&&q.get('topic'))topic.value=q.get('topic');
document.querySelectorAll('form[data-validate]').forEach(f=>{
 f.noValidate=true;
 const ok=f.parentElement.querySelector('.form-success');
 const msg=el=>{const v=el.validity;return v.valueMissing?(el.type==='checkbox'?'Please tick this box to continue.':'This field is required.'):v.patternMismatch?(el.dataset.msg||'Please check this value.'):v.typeMismatch?'Please enter a valid value.':(v.rangeUnderflow||v.rangeOverflow)?'Please enter a number within the allowed range.':v.badInput?'Please enter a valid value.':''};
 const show=el=>{const s=el.closest('.field')?.querySelector('.err');if(s)s.textContent=el.validity.valid?'':msg(el);el.setAttribute('aria-invalid',String(!el.validity.valid))};
 const clearErr=()=>f.querySelector('.form-error')?.remove();
 const showErr=t=>{clearErr();const d=document.createElement('div');d.className='form-error';d.setAttribute('role','alert');d.tabIndex=-1;d.textContent=t;f.querySelector('[type=submit]').before(d);d.focus()};
 f.addEventListener('focusout',e=>{if(e.target.willValidate)show(e.target)});
 f.addEventListener('input',e=>{if(e.target.willValidate&&e.target.getAttribute('aria-invalid')==='true')show(e.target)});
 f.addEventListener('submit',async e=>{
  e.preventDefault();clearErr();
  const els=[...f.elements].filter(el=>el.willValidate);
  els.forEach(show);
  const bad=els.find(el=>!el.validity.valid);
  if(bad){bad.focus();return}
  const btn=f.querySelector('[type=submit]'),label=btn.textContent;
  btn.disabled=true;btn.textContent='Sending…';
  const ctl=new AbortController(),t=setTimeout(()=>ctl.abort(),20000);
  try{
   const r=await fetch('/',{method:'POST',headers:{'Content-Type':'application/x-www-form-urlencoded'},body:new URLSearchParams(new FormData(f)).toString(),signal:ctl.signal});
   clearTimeout(t);
   if(!r.ok)throw new Error('HTTP '+r.status);
   f.hidden=true;ok.classList.add('show');ok.focus();   /* success is shown ONLY after a successful response */
  }catch(_){
   clearTimeout(t);btn.disabled=false;btn.textContent=label;
   showErr(f.dataset.fallback||'We could not send your request. Please try again.');
  }
 });
});
})();(()=>{
const R=matchMedia('(prefers-reduced-motion: reduce)').matches,de=document.documentElement;
/* Preloader: first visit per session only; never set when motion is reduced. CSS also auto-dismisses it if this script fails. */
if(de.classList.contains('pre-on')){
 setTimeout(()=>de.classList.add('pre-go'),1500);
 setTimeout(()=>de.classList.remove('pre-on','pre-go'),2500);
 try{sessionStorage.setItem('apexPre','1')}catch(_){}
}
const hd=document.querySelector('.site-header');
const onScroll=()=>hd&&hd.classList.toggle('scrolled',scrollY>12);
addEventListener('scroll',onScroll,{passive:true});onScroll();
if(R||!('IntersectionObserver' in window))return;
/* Scroll reveals (js-ready is set by the script above only when this is safe). Elements already in view start visible. */
const els=[...document.querySelectorAll('[data-r],[data-mask]')];
els.forEach(el=>{el.style.transitionDelay=(+el.dataset.r||0)*110+'ms';if(el.getBoundingClientRect().top<innerHeight*.9)el.classList.add('in')});
/* Position-based check (an IntersectionObserver ignores fully clipped elements, which would leave masked photos hidden). */
let pend=els.filter(el=>!el.classList.contains('in'));
const reveal=()=>{const vh=innerHeight;pend=pend.filter(el=>{const r=el.getBoundingClientRect();if(r.top<vh*.88&&r.bottom>0){el.classList.add('in');return false}return true})};
addEventListener('scroll',()=>requestAnimationFrame(reveal),{passive:true});addEventListener('resize',reveal);reveal();
/* Gentle parallax on photo frames, capped at 40px. */
const px=[...document.querySelectorAll('[data-parallax]')].map(f=>({f,i:[...f.querySelectorAll('img')],k:parseFloat(f.dataset.parallax)||.05}));
let busy=false;
const upd=()=>{busy=false;const vh=innerHeight;px.forEach(o=>{const r=o.f.getBoundingClientRect();if(r.bottom<-60||r.top>vh+60)return;const d=r.top+r.height/2-vh/2;{const y=Math.max(-40,Math.min(40,-d*o.k))+'px';o.i.forEach(i=>i.style.setProperty('--py',y))}})};
addEventListener('scroll',()=>{if(!busy){busy=true;requestAnimationFrame(upd)}},{passive:true});addEventListener('resize',upd);upd();
})();
(()=>{
const R=matchMedia('(prefers-reduced-motion: reduce)').matches;
/* Enquiry prefill from ?interest= (plain text only, capped). */
const q=new URLSearchParams(location.search),msg=document.querySelector('textarea[name=message]'),it=q.get('interest');
if(msg&&it&&!msg.value)msg.value='I would like to enquire about: '+it.slice(0,80);
/* Journey detail dialog. Without JS or <dialog> support, each card is simply a link to the enquiry form. */
const dlg=document.querySelector('.jd');
if(dlg&&typeof dlg.showModal==='function'){
 const fig=dlg.querySelector('.jd-fig'),body=dlg.querySelector('.jd-body'),h=dlg.querySelector('#jd-t'),enq=dlg.querySelector('.jd-enq'),more=dlg.querySelector('.jd-more');
 document.querySelectorAll('.jc').forEach(a=>a.addEventListener('click',e=>{
  e.preventDefault();
  h.textContent=a.dataset.title;
  body.replaceChildren(document.getElementById('j-'+a.dataset.j).content.cloneNode(true));
  const pic=a.querySelector('picture,img').cloneNode(true);
  [pic,...pic.querySelectorAll('img,source')].forEach(n=>{if(n.matches('img,source')){n.setAttribute('sizes','(min-width:760px) 430px, 94vw');if(n.matches('img'))n.loading='eager'}});
  fig.replaceChildren(pic);enq.href=a.href;more.href=a.dataset.page;
  dlg.showModal();document.documentElement.classList.add('jd-open');
 }));
 dlg.addEventListener('close',()=>document.documentElement.classList.remove('jd-open'));
 dlg.addEventListener('click',e=>{if(e.target===dlg)dlg.close()});
 dlg.querySelector('.jd-x').addEventListener('click',()=>dlg.close());
}
/* Sea video: loads only when near the viewport, never with reduced motion, Save-Data or 2G; paused off-screen; user pause control. */
const v=document.querySelector('.sea-v'),pb=document.querySelector('.sea-btn');
if(v&&pb){
 const c=navigator.connection||{};
 if(!R&&!c.saveData&&!/2g$/.test(c.effectiveType||'')&&'IntersectionObserver' in window){
  let on=false,user=false;
  new IntersectionObserver(es=>es.forEach(e=>{
   if(e.isIntersecting){if(!on){on=true;['mp4','webm'].forEach(x=>{const s=document.createElement('source');s.src=v.dataset[x];s.type='video/'+x;v.appendChild(s)});v.load()}if(!user)v.play().catch(()=>{})}else v.pause();
  }),{rootMargin:'200px'}).observe(v.parentElement);
  pb.hidden=false;
  pb.addEventListener('click',()=>{
   if(v.paused){user=false;v.play().catch(()=>{});pb.textContent='Pause';pb.setAttribute('aria-label','Pause background video')}
   else{user=true;v.pause();pb.textContent='Play';pb.setAttribute('aria-label','Play background video')}
  });
 }
}
})();
