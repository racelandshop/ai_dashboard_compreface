import{_ as i,s as o,e as t,t as a,f as e,$ as l,l as s,m as n,a as r,c as d,d as p,r as c,n as h}from"./main-cd61fc31.js";import"./c.5a85e488.js";let g=i([h("upload-ai-facial-data-dialog")],(function(i,o){return{F:class extends o{constructor(...o){super(...o),i(this)}},d:[{kind:"field",decorators:[t({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[t()],key:"url_list",value:void 0},{kind:"field",decorators:[t({attribute:!1})],key:"personInfo",value:void 0},{kind:"field",decorators:[t()],key:"uploadErrorMessage",value:void 0},{kind:"field",decorators:[a()],key:"_params",value:void 0},{kind:"method",key:"showDialog",value:async function(i){this._params=i,this.personInfo=i.personInfo}},{kind:"method",key:"closeDialog",value:function(){this._params=void 0,this.url_list=void 0,this.uploadErrorMessage=void 0,e(this,"dialog-closed",{dialog:this.localName})}},{kind:"method",key:"render",value:function(){return this._params?l`
      <ha-dialog
        open
        scrimClickAction
        hideActions
        .heading=${s("common.upload_facial_data")}
        @closed=${this.closeDialog}
      >
        <div class="header" slot="heading">
          <ha-svg-icon
            dialogAction="close"
            class="cancel-icon"
            slot="icon"
            .path=${n}
          ></ha-svg-icon>
          <ha-svg-icon class="header-icon" slot="icon" .path=${r}></ha-svg-icon>
        </div>
        <div class="text">
        ${void 0===this.url_list&&void 0===this.uploadErrorMessage?l`<p class="big-text">${s("dialog_text.upload_message")}</p>`:void 0!==this.url_list?l`<p class="big-text">
                ${s("dialog_text.upload_photo_n","{n_photos}",String(this.url_list.length))}
              </p>`:l`<p class="error-text-small">${this.uploadErrorMessage}</p>`}
          <p class="small-text">${s("dialog_text.upload_message_note")}</p>
          </p>
        </div>
        <div class="options">
        <file-upload class="button-upload"
          .hass=${this.hass}
          @files-url-generated=${this._handleFilePicked}
          accept="image/png, image/jpeg, image/gif"
          >
        </file-upload>
          ${void 0===this.url_list?l``:l` <mwc-button class="button-confirm" @click=${this._confirm}
                  ><ha-svg-icon
                    .path=${d}
                    class="confirm-icon"
                    slot="icon"
                  ></ha-svg-icon
                  >${s("common.confirm")}</mwc-button
                >`}
        </div>
      </ha-dialog>
    `:l``}},{kind:"method",key:"_handleFilePicked",value:async function(i){this.url_list=i.detail.url_list,this.uploadErrorMessage=void 0}},{kind:"method",key:"_confirm",value:async function(){if(null!=this.url_list){var i;!0===await p(this.hass,null===(i=this.personInfo)||void 0===i?void 0:i.name,this.url_list)?(e(this,"update-ai-dashboard"),this.closeDialog()):(this.url_list=void 0,this.uploadErrorMessage=s("error.teachFaceErrorMessage"))}}},{kind:"get",static:!0,key:"styles",value:function(){return[c`
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
      `]}}]}}),o);export{g as HuiDialogAddAiFacialData};
