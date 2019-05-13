import { Injectable } from '@angular/core';
// import { Http, Response } from '@angular/http';
import { HttpClient, HttpParams } from "@angular/common/http";

import { Observable } from 'rxjs/Observable';

import { LogLine, RefGroup, RefDir, RefFile, Sample, ActiveTask, HistoryTask } from '../models/models'
import { PeSection, PeImportDllTable } from '../models/models-pe';

@Injectable()
export class ServerDataService {

  baseUrl: string = 'http://127.0.0.1:5000'

  constructor(private _http: HttpClient) {

  }

  // -----------------------------------------------------------------------------------

  // test

  cmdTest() {
    this._http.post(this.baseUrl + "/test/", {
      "action": "test",
    }).subscribe();
  }

  getTest(): Observable<any[]> {
    let params = new HttpParams();
    params = params.append("action", 'test');

    return this._http.get<any[]>(this.baseUrl + "/test/", { params: params });
  }

  // -----------------------------------------------------------------------------------

  // get logLine list
  getLogLines(isWarn: boolean, isDebug: boolean): Observable<LogLine[]> {
    let params = new HttpParams();
    params = params.append("action", 'get_logLines');

    params = params.append("isWarn", `${isWarn}`);
    params = params.append("isDebug", `${isDebug}`);

    return this._http.get<LogLine[]>(this.baseUrl + "/logline/", { params: params });
  }

  // clear log lines
  clearLogLines() {
    // .subscribe() is necessary to truely "send" this request!!!
    this._http.post(this.baseUrl + "/logline/", {
      "action": "clearLogLines",
    }).subscribe();
  }

  // -----------------------------------------------------------------------------------

  // get list stuff

  // get all RefGroup list
  getGroupList(pageSize: number, pageIndex: number): Observable<RefGroup[]> {
    let params = new HttpParams();
    params = params.append("action", 'get_refGroupList');

    params = params.append("pageSize", `${pageSize}`);
    params = params.append("pageIndex", `${pageIndex}`);

    return this._http.get<RefGroup[]>(this.baseUrl + "/tree/", { params: params });
  }

  // get top refDir by group_id
  getTopRefDir(group_id: string): Observable<RefDir[]> {
    let params = new HttpParams();
    params = params.append("action", 'get_topRefDirs');

    params = params.append("group_id", group_id);

    return this._http.get<RefDir[]>(this.baseUrl + "/tree/", { params: params });
  }

  // get sub RefDir by RefDirId
  getSubRefDirs(refDir_id: string): Observable<RefDir[]> {
    let params = new HttpParams();
    params = params.append("action", 'get_subRefDirs');

    params = params.append("refDir_id", refDir_id);

    return this._http.get<RefDir[]>(this.baseUrl + "/tree/", { params: params });
  }

  // get sub Sample by RefDirId
  getSubSamples(refDir_id: string): Observable<Sample[]> {
    let params = new HttpParams();
    params = params.append("action", 'get_subSamples');

    params = params.append("refDir_id", refDir_id);

    return this._http.get<Sample[]>(this.baseUrl + "/tree/", { params: params });
  }


  // get sub refFile by RefDirId
  getSubRefFiles(refDir_id: string): Observable<RefFile[]> {
    let params = new HttpParams();
    params = params.append("action", 'get_subRefFiles');

    params = params.append("refDir_id", refDir_id);

    return this._http.get<RefFile[]>(this.baseUrl + "/tree/", { params: params });
  }

  // del ref dir
  cmdDeleteRefDir(refDir_id: string) {
    return this._http.post(this.baseUrl + "/tree/", {
      "action": "deleteRefDir",
      "refDirId": refDir_id
    });
  }

  cmdClearTree() {
    return this._http.post(this.baseUrl + "/tree/", {
      "action": "clearTree",
    });
  }

  // -----------------------------------------------------------------------------------

  // sample/file

  // analyze file as sample
  cmdAnalyzeSample(refFile_id: string) {
    this._http.post(this.baseUrl + "/reffile/", {
      "action": "analyzeAsSample",
      "refFileId": refFile_id
    }).subscribe();
  }

  // pe

  // get header info
  getPeHeaderInfo(sample_id: string): Observable<any[]>{
      let params = new HttpParams();
      params = params.append("action", 'get_HeaderInfo');
      params = params.append("sample_id", sample_id);

      return this._http.get<any[]>(this.baseUrl + "/pe/", { params: params });
  }

  // get header info
  getPeSectionInfo(sample_id: string): Observable<PeSection[]>{
      let params = new HttpParams();
      params = params.append("action", 'get_SectionInfo');
      params = params.append("sample_id", sample_id);

      return this._http.get<PeSection[]>(this.baseUrl + "/pe/", { params: params });
  }

  // get header info
  getPeImportInfo(sample_id: string): Observable<PeImportDllTable[]>{
      let params = new HttpParams();
      params = params.append("action", 'get_ImportInfo');
      params = params.append("sample_id", sample_id);

      return this._http.get<PeImportDllTable[]>(this.baseUrl + "/pe/", { params: params });
  }

  // get header info
  getPeExportInfo(sample_id: string): Observable<any[]>{
      let params = new HttpParams();
      params = params.append("action", 'get_ExportInfo');
      params = params.append("sample_id", sample_id);

      return this._http.get<any[]>(this.baseUrl + "/pe/", { params: params });
  }

  // get header info
  getPeBehvFileInfo(sample_id: string): Observable<any[]>{
      let params = new HttpParams();
      params = params.append("action", 'get_BehvFileInfo');
      params = params.append("sample_id", sample_id);

      return this._http.get<any[]>(this.baseUrl + "/pe/", { params: params });
  }

  // -----------------------------------------------------------------------------------

  // task

  // get task list
  getTaskList(): Observable<any[]> {
    let params = new HttpParams();
    params = params.append("action", 'get_TaskList');

    return this._http.get<any[]>(this.baseUrl + "/task/", { params: params });
  }

  // cancel task
  cmdCancelTask(taskId: string) {
    this._http.post(this.baseUrl + "/task/", {
      "action": "cancelTask",
      "taskId": taskId,
    }).subscribe();
  }


}
