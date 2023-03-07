import{_ as i,s as t,e as o,t as a,f as e,$ as l,l as n,m as s,a as r,b as d,c,d as h,g as p,r as m,n as g}from"./main-cd61fc31.js";import"./c.5a85e488.js";let x=i([g("update-ai-facial-data-dialog")],(function(i,t){return{F:class extends t{constructor(...t){super(...t),i(this)}},d:[{kind:"field",decorators:[o({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[o({attribute:!1})],key:"personInfo",value:void 0},{kind:"field",decorators:[o()],key:"url_list",value:void 0},{kind:"field",decorators:[o()],key:"uploadErrorMessage",value:void 0},{kind:"field",decorators:[a()],key:"_params",value:void 0},{kind:"method",key:"showDialog",value:async function(i){this._params=i,this.personInfo=i.personInfo}},{kind:"method",key:"closeDialog",value:function(){this._params=void 0,this.url_list=void 0,this.uploadErrorMessage=void 0,e(this,"dialog-closed",{dialog:this.localName})}},{kind:"method",key:"render",value:function(){return this._params?l`
      <ha-dialog
        open
        scrimClickAction
        hideActions
        .heading=${n("common.update_facial_data")}
        @closed=${this.closeDialog}
      >
        <div class="header" slot="heading">
          <ha-svg-icon
            dialogAction="close"
            class="cancel-icon"
            slot="icon"
            .path=${s}
          ></ha-svg-icon>
          <ha-svg-icon class="header-icon" slot="icon" .path=${r}></ha-svg-icon>
        </div>
        <div class="text">
          ${void 0===this.url_list&&void 0===this.uploadErrorMessage?l`<p class="big-text">${n("common.update_facial_data")}</p>`:void 0!==this.url_list?l`<p class="big-text">
                ${n("dialog_text.upload_photo_n","{n_photos}",String(this.url_list.length))}
              </p>`:l`<p class="error-text-small">${this.uploadErrorMessage}</p>`}
          <p class="small-text">${n("dialog_text.verify_action")}</p>
        </div>
        <div class="options">
          <file-upload
            class="button-upload"
            .hass=${this.hass}
            @files-url-generated=${this._handleFilePicked}
            accept="image/png, image/jpeg, image/gif"
          >
          </file-upload>
          ${void 0===this.url_list?l`<mwc-button class="button-delete" @click=${this._delete}
                ><ha-svg-icon class="confirm-icon" slot="icon" .path=${d}></ha-svg-icon
                >${n("common.delete")}</mwc-button
              >`:l`<mwc-button class="button-confirm" @click=${this._confirm}
                ><ha-svg-icon
                  .path=${c}
                  class="confirm-icon"
                  slot="icon"
                ></ha-svg-icon
                >${n("common.confirm")}</mwc-button
              >`}
        </div>
      </ha-dialog>
    `:l``}},{kind:"method",key:"_handleFilePicked",value:async function(i){this.url_list=i.detail.url_list,this.uploadErrorMessage=void 0}},{kind:"method",key:"_confirm",value:async function(){if(null!=this.url_list){var i;!0===await h(this.hass,null===(i=this.personInfo)||void 0===i?void 0:i.name,this.url_list)?(e(this,"update-ai-dashboard"),this.closeDialog()):(this.url_list=void 0,this.uploadErrorMessage=n("error.teachFaceErrorMessage"))}}},{kind:"method",key:"_delete",value:async function(i){var t;i&&i.stopPropagation();!0===await p(this.hass,null===(t=this.personInfo)||void 0===t?void 0:t.name)&&(e(this,"update-ai-dashboard"),this.closeDialog())}},{kind:"get",static:!0,key:"styles",value:function(){return[m`
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
          border-bottom: none;
        }
        .button-upload {
          background-color: #4ba2ff;
          float: left;
        }
        .button-confirm {
          background-color: #4ba2ff;
          float: right;
        }
        .button-delete {
          background-color: #4ba2ff;
          float: right;
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
        .cancel-icon {
          float: right;
          width: 40px;
          height: 40px;
          cursor: pointer;
          padding: 20px 20px 20px 20px;
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
      `]}}]}}),t);export{x as HuiDeleteDialogAiFacialData};
