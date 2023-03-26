import{h as r,e,i,s as t,$ as a,q as s,F as c,u as o,r as n,n as d,_ as l,C as p,D as m,t as g,f as h,l as u,m as f,a as y,c as _,d as x}from"./main-56b9c346.js";import"./c.4f571bb8.js";class v extends t{constructor(){super(...arguments),this.indeterminate=!1,this.progress=0,this.density=0,this.closed=!1}open(){this.closed=!1}close(){this.closed=!0}render(){const r={"mdc-circular-progress--closed":this.closed,"mdc-circular-progress--indeterminate":this.indeterminate},e=48+4*this.density,i={width:`${e}px`,height:`${e}px`};return a`
      <div
        class="mdc-circular-progress ${s(r)}"
        style="${c(i)}"
        role="progressbar"
        aria-label="${o(this.ariaLabel)}"
        aria-valuemin="0"
        aria-valuemax="1"
        aria-valuenow="${o(this.indeterminate?void 0:this.progress)}">
        ${this.renderDeterminateContainer()}
        ${this.renderIndeterminateContainer()}
      </div>`}renderDeterminateContainer(){const r=48+4*this.density,e=r/2,i=this.density>=-3?18+11*this.density/6:12.5+5*(this.density+3)/4,t=6.2831852*i,s=(1-this.progress)*t,c=this.density>=-3?4+this.density*(1/3):3+(this.density+3)*(1/6);return a`
      <div class="mdc-circular-progress__determinate-container">
        <svg class="mdc-circular-progress__determinate-circle-graphic"
             viewBox="0 0 ${r} ${r}">
          <circle class="mdc-circular-progress__determinate-track"
                  cx="${e}" cy="${e}" r="${i}"
                  stroke-width="${c}"></circle>
          <circle class="mdc-circular-progress__determinate-circle"
                  cx="${e}" cy="${e}" r="${i}"
                  stroke-dasharray="${6.2831852*i}"
                  stroke-dashoffset="${s}"
                  stroke-width="${c}"></circle>
        </svg>
      </div>`}renderIndeterminateContainer(){return a`
      <div class="mdc-circular-progress__indeterminate-container">
        <div class="mdc-circular-progress__spinner-layer">
          ${this.renderIndeterminateSpinnerLayer()}
        </div>
      </div>`}renderIndeterminateSpinnerLayer(){const r=48+4*this.density,e=r/2,i=this.density>=-3?18+11*this.density/6:12.5+5*(this.density+3)/4,t=6.2831852*i,s=.5*t,c=this.density>=-3?4+this.density*(1/3):3+(this.density+3)*(1/6);return a`
        <div class="mdc-circular-progress__circle-clipper mdc-circular-progress__circle-left">
          <svg class="mdc-circular-progress__indeterminate-circle-graphic"
               viewBox="0 0 ${r} ${r}">
            <circle cx="${e}" cy="${e}" r="${i}"
                    stroke-dasharray="${t}"
                    stroke-dashoffset="${s}"
                    stroke-width="${c}"></circle>
          </svg>
        </div>
        <div class="mdc-circular-progress__gap-patch">
          <svg class="mdc-circular-progress__indeterminate-circle-graphic"
               viewBox="0 0 ${r} ${r}">
            <circle cx="${e}" cy="${e}" r="${i}"
                    stroke-dasharray="${t}"
                    stroke-dashoffset="${s}"
                    stroke-width="${.8*c}"></circle>
          </svg>
        </div>
        <div class="mdc-circular-progress__circle-clipper mdc-circular-progress__circle-right">
          <svg class="mdc-circular-progress__indeterminate-circle-graphic"
               viewBox="0 0 ${r} ${r}">
            <circle cx="${e}" cy="${e}" r="${i}"
                    stroke-dasharray="${t}"
                    stroke-dashoffset="${s}"
                    stroke-width="${c}"></circle>
          </svg>
        </div>`}update(r){super.update(r),r.has("progress")&&(this.progress>1&&(this.progress=1),this.progress<0&&(this.progress=0))}}r([e({type:Boolean,reflect:!0})],v.prototype,"indeterminate",void 0),r([e({type:Number,reflect:!0})],v.prototype,"progress",void 0),r([e({type:Number,reflect:!0})],v.prototype,"density",void 0),r([e({type:Boolean,reflect:!0})],v.prototype,"closed",void 0),r([i,e({type:String,attribute:"aria-label"})],v.prototype,"ariaLabel",void 0);const b=n`.mdc-circular-progress__determinate-circle,.mdc-circular-progress__indeterminate-circle-graphic{stroke:#6200ee;stroke:var(--mdc-theme-primary, #6200ee)}.mdc-circular-progress__determinate-track{stroke:transparent}@keyframes mdc-circular-progress-container-rotate{to{transform:rotate(360deg)}}@keyframes mdc-circular-progress-spinner-layer-rotate{12.5%{transform:rotate(135deg)}25%{transform:rotate(270deg)}37.5%{transform:rotate(405deg)}50%{transform:rotate(540deg)}62.5%{transform:rotate(675deg)}75%{transform:rotate(810deg)}87.5%{transform:rotate(945deg)}100%{transform:rotate(1080deg)}}@keyframes mdc-circular-progress-color-1-fade-in-out{from{opacity:.99}25%{opacity:.99}26%{opacity:0}89%{opacity:0}90%{opacity:.99}to{opacity:.99}}@keyframes mdc-circular-progress-color-2-fade-in-out{from{opacity:0}15%{opacity:0}25%{opacity:.99}50%{opacity:.99}51%{opacity:0}to{opacity:0}}@keyframes mdc-circular-progress-color-3-fade-in-out{from{opacity:0}40%{opacity:0}50%{opacity:.99}75%{opacity:.99}76%{opacity:0}to{opacity:0}}@keyframes mdc-circular-progress-color-4-fade-in-out{from{opacity:0}65%{opacity:0}75%{opacity:.99}90%{opacity:.99}to{opacity:0}}@keyframes mdc-circular-progress-left-spin{from{transform:rotate(265deg)}50%{transform:rotate(130deg)}to{transform:rotate(265deg)}}@keyframes mdc-circular-progress-right-spin{from{transform:rotate(-265deg)}50%{transform:rotate(-130deg)}to{transform:rotate(-265deg)}}.mdc-circular-progress{display:inline-flex;position:relative;direction:ltr;line-height:0;transition:opacity 250ms 0ms cubic-bezier(0.4, 0, 0.6, 1)}.mdc-circular-progress__determinate-container,.mdc-circular-progress__indeterminate-circle-graphic,.mdc-circular-progress__indeterminate-container,.mdc-circular-progress__spinner-layer{position:absolute;width:100%;height:100%}.mdc-circular-progress__determinate-container{transform:rotate(-90deg)}.mdc-circular-progress__indeterminate-container{font-size:0;letter-spacing:0;white-space:nowrap;opacity:0}.mdc-circular-progress__determinate-circle-graphic,.mdc-circular-progress__indeterminate-circle-graphic{fill:transparent}.mdc-circular-progress__determinate-circle{transition:stroke-dashoffset 500ms 0ms cubic-bezier(0, 0, 0.2, 1)}.mdc-circular-progress__gap-patch{position:absolute;top:0;left:47.5%;box-sizing:border-box;width:5%;height:100%;overflow:hidden}.mdc-circular-progress__gap-patch .mdc-circular-progress__indeterminate-circle-graphic{left:-900%;width:2000%;transform:rotate(180deg)}.mdc-circular-progress__circle-clipper{display:inline-flex;position:relative;width:50%;height:100%;overflow:hidden}.mdc-circular-progress__circle-clipper .mdc-circular-progress__indeterminate-circle-graphic{width:200%}.mdc-circular-progress__circle-right .mdc-circular-progress__indeterminate-circle-graphic{left:-100%}.mdc-circular-progress--indeterminate .mdc-circular-progress__determinate-container{opacity:0}.mdc-circular-progress--indeterminate .mdc-circular-progress__indeterminate-container{opacity:1}.mdc-circular-progress--indeterminate .mdc-circular-progress__indeterminate-container{animation:mdc-circular-progress-container-rotate 1568.2352941176ms linear infinite}.mdc-circular-progress--indeterminate .mdc-circular-progress__spinner-layer{animation:mdc-circular-progress-spinner-layer-rotate 5332ms cubic-bezier(0.4, 0, 0.2, 1) infinite both}.mdc-circular-progress--indeterminate .mdc-circular-progress__color-1{animation:mdc-circular-progress-spinner-layer-rotate 5332ms cubic-bezier(0.4, 0, 0.2, 1) infinite both,mdc-circular-progress-color-1-fade-in-out 5332ms cubic-bezier(0.4, 0, 0.2, 1) infinite both}.mdc-circular-progress--indeterminate .mdc-circular-progress__color-2{animation:mdc-circular-progress-spinner-layer-rotate 5332ms cubic-bezier(0.4, 0, 0.2, 1) infinite both,mdc-circular-progress-color-2-fade-in-out 5332ms cubic-bezier(0.4, 0, 0.2, 1) infinite both}.mdc-circular-progress--indeterminate .mdc-circular-progress__color-3{animation:mdc-circular-progress-spinner-layer-rotate 5332ms cubic-bezier(0.4, 0, 0.2, 1) infinite both,mdc-circular-progress-color-3-fade-in-out 5332ms cubic-bezier(0.4, 0, 0.2, 1) infinite both}.mdc-circular-progress--indeterminate .mdc-circular-progress__color-4{animation:mdc-circular-progress-spinner-layer-rotate 5332ms cubic-bezier(0.4, 0, 0.2, 1) infinite both,mdc-circular-progress-color-4-fade-in-out 5332ms cubic-bezier(0.4, 0, 0.2, 1) infinite both}.mdc-circular-progress--indeterminate .mdc-circular-progress__circle-left .mdc-circular-progress__indeterminate-circle-graphic{animation:mdc-circular-progress-left-spin 1333ms cubic-bezier(0.4, 0, 0.2, 1) infinite both}.mdc-circular-progress--indeterminate .mdc-circular-progress__circle-right .mdc-circular-progress__indeterminate-circle-graphic{animation:mdc-circular-progress-right-spin 1333ms cubic-bezier(0.4, 0, 0.2, 1) infinite both}.mdc-circular-progress--closed{opacity:0}:host{display:inline-flex}.mdc-circular-progress__determinate-track{stroke:transparent;stroke:var(--mdc-circular-progress-track-color, transparent)}`;let k=class extends v{};k.styles=[b],k=r([d("mwc-circular-progress")],k),l([d("ha-circular-progress")],(function(r,i){class t extends i{constructor(...e){super(...e),r(this)}}return{F:t,d:[{kind:"field",decorators:[e({type:Boolean})],key:"active",value:()=>!1},{kind:"field",decorators:[e()],key:"alt",value:()=>"Loading"},{kind:"field",decorators:[e()],key:"size",value:()=>"medium"},{kind:"set",key:"density",value:function(r){}},{kind:"get",key:"density",value:function(){switch(this.size){case"tiny":return-8;case"small":return-5;case"medium":default:return 0;case"large":return 5}}},{kind:"set",key:"indeterminate",value:function(r){}},{kind:"get",key:"indeterminate",value:function(){return this.active}},{kind:"get",static:!0,key:"styles",value:function(){return[p(m(t),"styles",this),n`
        :host {
          overflow: hidden;
        }
      `]}}]}}),k);let $=l([d("upload-ai-facial-data-dialog")],(function(r,i){return{F:class extends i{constructor(...e){super(...e),r(this)}},d:[{kind:"field",decorators:[e({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[e()],key:"url_list",value:void 0},{kind:"field",decorators:[e({attribute:!1})],key:"personInfo",value:void 0},{kind:"field",decorators:[e()],key:"uploadErrorMessage",value:void 0},{kind:"field",decorators:[g()],key:"_params",value:void 0},{kind:"field",decorators:[g()],key:"uploading",value:()=>!1},{kind:"method",key:"showDialog",value:async function(r){this._params=r,this.personInfo=r.personInfo}},{kind:"method",key:"closeDialog",value:function(){this._params=void 0,this.url_list=void 0,this.uploadErrorMessage=void 0,h(this,"dialog-closed",{dialog:this.localName})}},{kind:"method",key:"render",value:function(){return this._params?a`
      <ha-dialog
        open
        scrimClickAction
        hideActions
        .heading=${u("common.upload_facial_data")}
        @closed=${this.closeDialog}
      >
        <div class="header" slot="heading">
          <ha-svg-icon
            dialogAction="close"
            class="cancel-icon"
            slot="icon"
            .path=${f}
          ></ha-svg-icon>
          <ha-svg-icon class="header-icon" slot="icon" .path=${y}></ha-svg-icon>
        </div>
        <div class="text">
        ${void 0===this.url_list&&void 0===this.uploadErrorMessage?a`<p class="big-text">${u("dialog_text.upload_message")}</p>`:void 0!==this.url_list?a`<p class="big-text">
                ${u("dialog_text.upload_photo_n","{n_photos}",String(this.url_list.length))}
              </p>`:a`<p class="error-text-small">${this.uploadErrorMessage}</p>`}
          <p class="small-text">${u("dialog_text.upload_message_note")}</p>
          </p>
        </div>
        <div class="options">
        <file-upload class="button-upload"
          .hass=${this.hass}
          @files-url-generated=${this._handleFilePicked}
          accept="image/png, image/jpeg, image/gif"
          >
        </file-upload>
        ${void 0===this.url_list?a``:a`
                ${this.uploading?a`<div class="upload-progress">
                      <ha-circular-progress active></ha-circular-progress>
                    </div>`:a`<mwc-button class="button-confirm" @click=${this._confirm}
                      ><ha-svg-icon
                        .path=${_}
                        class="confirm-icon"
                        slot="icon"
                      ></ha-svg-icon
                      >${u("common.confirm")}</mwc-button
                    >`}
              `}
        </div>
      </ha-dialog>
    `:a``}},{kind:"method",key:"_handleFilePicked",value:async function(r){this.url_list=r.detail.url_list,this.uploadErrorMessage=void 0}},{kind:"method",key:"_confirm",value:async function(){if(null!=this.url_list){var r;this.uploading=!0;!0===await x(this.hass,null===(r=this.personInfo)||void 0===r?void 0:r.name,this.url_list)?(h(this,"update-ai-dashboard"),this.uploading=!1,this.closeDialog()):(this.url_list=void 0,this.uploading=!1,this.uploadErrorMessage=u("error.teachFaceErrorMessage"))}}},{kind:"get",static:!0,key:"styles",value:function(){return[n`
        @media all and (max-width: 450px), all and (max-height: 500px) {
          /* overrule the ha-style-dialog max-height on small screens */
          ha-dialog {
            --mdc-dialog-max-height: 100%;
            height: 100%;
          }
        }
        @media all and (min-width: 800px) {
          ha-dialog {
            --mdc-dialog-min-width: 500px;
          }
        }
        @media all and (max-width: 450px), all and (max-height: 500px) {
          hui-entity-picker-table {
            height: calc(100vh - 158px);
          }
        }
        ha-dialog {
          --mdc-dialog-max-width: 500px;
          --dialog-content-padding: 2px 24px 20px 24px;
          --dialog-z-index: 5;
        }
        ha-header-bar {
          --mdc-theme-on-primary: var(--primary-text-color);
          --mdc-theme-primary: var(--mdc-theme-surface);
          flex-shrink: 0;
          border-bottom: 1px solid var(--mdc-dialog-scroll-divider-color, rgba(0, 0, 0, 0.12));
        }
        file-upload {
          padding: 10px;
          text-align: center;
          text-decoration: none;
          display: inline-block;
          font-size: 16px;
          margin: 4px 2px;
          border-radius: 30px;
          box-shadow: 0px 0px 5px 0px rgba(1, 1, 1, 0);
          --mdc-theme-primary: white;
          margin-bottom: 40px;
        }
        mwc-button {
          padding: 10px;
          text-align: center;
          text-decoration: none;
          display: inline-block;
          font-size: 16px;
          margin: 4px 2px;
          border-radius: 30px;
          cursor: pointer;
          box-shadow: 0px 0px 5px 0px rgba(1, 1, 1, 0);
          --mdc-theme-primary: white;
          margin-bottom: 40px;
        }
        .upload-progress {
          float: right;
          margin-right: 8px;
          font-size: 8px;
        }
        .button-confirm {
          background-color: #4ba2ff;
          float: right;
        }
        .button-upload {
          float: left;
          background-color: #4ba2ff;
        }
        input.file {
          display: none;
        }
        label.mdc-field {
          cursor: pointer;
        }
        .header {
          height: 80px;
        }
        .cancel-icon {
          float: right;
          width: 40px;
          height: 40px;
          cursor: pointer;
          padding: 20px 20px 20px 20px;
        }
        .options {
          width: 100%;
        }
        .confirm-icon {
          width: 20px;
          height: 40px;
        }
        .header-icon {
          width: 60px;
          height: 60px;
          margin-top: 10%;
          margin-bottom: 10%;
          margin-left: 6%;
          color: #7b7b7b;
        }
        .text {
          margin-top: 10%;
          width: 100%;
          margin: 0px 0px 20px 0px;
        }
        .big-text {
          font-family: "Roboto";
          font-style: normal;
          font-weight: 500;
          font-size: 24px;
          line-height: 42px;
          color: #303033;
          margin: 10px;
        }
        .small-text {
          font-family: "Roboto";
          font-style: normal;
          font-weight: 400;
          font-size: 24px;
          line-height: 21px;
          color: gray;
          margin: 10px;
        }
        .error-text-small {
          margin-top: 10%;
          font-family: "Roboto";
          font-style: normal;
          font-weight: 400;
          font-size: 24px;
          line-height: 21px;
          color: red;
          text-align: justify;
          text-justify: inter-word;
        }
      `]}}]}}),t);export{$ as HuiDialogAddAiFacialData};
