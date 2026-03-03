# Task 範本
TASK_TEMPLATE = {
    "ALM-Service":{
        "TFS需求申請或調整": {
            "Feature": {
                "template_use_description": [
                    ["建立CD管線(正式環境)", "李小姐"]
                ],
                "template_info": [
                    {
                        "title": "[{project_name}] 請協助建置 Release Project 正式環境 CD 流程",
                        "description": 
                            """
                            <div><span><b style="box-sizing:border-box;color:rgb(12, 136, 42);background-color:rgb(255, 255, 255);">（<b
                                            style="box-sizing:border-box;background-color:rgb(255, 255, 255);">請於此寫下申請之資訊</b>）</b></span></div>
                            <div><span>1. 申請原因：</span><span style="color:rgb(12, 100, 192);">{reason}</span><span><br></span></div>
                            <div>2. 上線日期：<span style="color:rgb(12, 100, 192);">{online_date}</span><br></div>
                            <div>3. 承辦人員：<span style="color:rgb(12, 100, 192);">{user}</span><br></div>
                            <div>4. 系統名稱：<span style="color:rgb(12, 100, 192);">{apid_name}</span><br></div>
                            <div>
                                5. TFS專案名稱：<span style="color:rgb(12, 100, 192);">{project_name}</span><br></div>
                            <div>
                                6. APID：<span style="color:rgb(12, 100, 192);">{apid}</span><br></div>
                            <div>
                                7. 管線路徑：</div>
                            <div><span style="color:rgb(12, 100, 192);">{pipeline_path}</span></div>
                            <div><span style="color:rgb(12, 100, 192);">{pipeline_link}</span></div>
                            8. 變數群組：{variable_group}</div>
                            <br></div>
                        """,
                        "tags": ["{project_name}"],
                        "parameter": {"project_name": "TFS專案名稱",
                                      "reason": "申請原因", 
                                      "online_date": "YYYY/MM/DD", 
                                      "pipeline_path": "管線路徑", 
                                      "pipeline_link": "管線連結", 
                                      "variable_group": "變數群組", 
                                      "other_description": "其他說明"}
                    }
                ]
            }
        }
    }
}