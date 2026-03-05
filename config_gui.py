import json
import os
import tkinter as tk
from tkinter import ttk, messagebox

class ConfigGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("OpenClaw 配置修改工具")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # 配置文件路径
        self.config_path = 'openclaw.json'
        self.config = None
        
        # 创建主框架
        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 创建顶部按钮框架
        self.button_frame = ttk.Frame(self.main_frame)
        self.button_frame.pack(fill=tk.X, pady=5)
        
        # 选择文件按钮
        self.select_file_btn = ttk.Button(self.button_frame, text="选择文件", command=self.select_file)
        self.select_file_btn.pack(side=tk.LEFT, padx=5)
        
        # 保存配置按钮
        self.save_btn = ttk.Button(self.button_frame, text="保存配置", command=self.save_config, state=tk.DISABLED)
        self.save_btn.pack(side=tk.LEFT, padx=5)
        
        # 退出按钮
        self.exit_btn = ttk.Button(self.button_frame, text="退出", command=root.quit)
        self.exit_btn.pack(side=tk.RIGHT, padx=5)
        
        # 文件路径显示
        self.file_path_var = tk.StringVar(value=self.config_path)
        self.file_path_label = ttk.Label(self.main_frame, text="当前文件:")
        self.file_path_label.pack(anchor=tk.W, pady=5)
        self.file_path_entry = ttk.Entry(self.main_frame, textvariable=self.file_path_var, state="readonly")
        self.file_path_entry.pack(fill=tk.X, pady=5)
        
        # 状态显示区域
        self.status_var = tk.StringVar(value="就绪")
        self.status_frame = ttk.Frame(self.main_frame)
        self.status_frame.pack(fill=tk.X, pady=10, side=tk.BOTTOM)
        ttk.Label(self.status_frame, text="状态:", font=("Arial", 10)).pack(side=tk.LEFT, padx=5)
        ttk.Label(self.status_frame, textvariable=self.status_var, font=("Arial", 10), foreground="#333").pack(side=tk.LEFT, padx=5)
        
        # 创建笔记本（标签页）
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # 创建各个标签页
        self.meta_tab = ttk.Frame(self.notebook)
        self.models_tab = ttk.Frame(self.notebook)
        self.agents_tab = ttk.Frame(self.notebook)
        self.gateway_tab = ttk.Frame(self.notebook)
        
        # 添加标签页
        self.notebook.add(self.meta_tab, text="元数据")
        self.notebook.add(self.models_tab, text="模型配置")
        self.notebook.add(self.agents_tab, text="代理配置")
        self.notebook.add(self.gateway_tab, text="网关配置")
        
        # 初始化各个标签页的内容
        self.init_meta_tab()
        self.init_models_tab()
        self.init_agents_tab()
        self.init_gateway_tab()
        
        # 初始加载配置
        self.load_config()
    
    def select_file(self):
        """选择配置文件"""
        from tkinter import filedialog
        import os
        # 获取用户的.openclaw目录
        user_home = os.path.expanduser('~')
        default_dir = os.path.join(user_home, '.openclaw')
        # 确保目录存在
        if not os.path.exists(default_dir):
            os.makedirs(default_dir)
        
        file_path = filedialog.askopenfilename(
            title="选择配置文件",
            filetypes=[("JSON文件", "*.json"), ("所有文件", "*.*")],
            initialdir=default_dir
        )
        if file_path:
            # 创建带日期的备份文件
            import datetime
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = f"{file_path}.{timestamp}.bak"
            try:
                import shutil
                shutil.copy2(file_path, backup_path)
                self.status_var.set(f"已选择文件: {os.path.basename(file_path)} (已备份)")
            except Exception as e:
                self.status_var.set(f"已选择文件: {os.path.basename(file_path)} (备份失败: {e})")
            
            self.config_path = file_path
            self.file_path_var.set(file_path)
            # 自动加载配置
            self.load_config()
    
    def load_config(self):
        """加载配置文件"""
        if not os.path.exists(self.config_path):
            self.status_var.set("错误: 配置文件不存在！")
            return
        
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
            
            # 更新各个标签页的内容
            self.update_meta_tab()
            self.update_models_tab()
            self.update_agents_tab()
            self.update_gateway_tab()
            
            self.save_btn.config(state=tk.NORMAL)
            self.status_var.set("配置文件加载成功")
        except json.JSONDecodeError as e:
            self.status_var.set(f"错误: 配置文件解析错误: {e}")
        except Exception as e:
            self.status_var.set(f"错误: 加载配置文件失败: {e}")
    

    
    def save_config(self):
        """保存配置文件"""
        if not self.config:
            messagebox.showwarning("警告", "请先加载配置文件！")
            return
        
        try:
            # 从各个标签页获取修改后的值
            self.get_meta_values()
            self.get_models_values()
            self.get_agents_values()
            self.get_gateway_values()
            
            # 强制更新代理配置中的主模型
            provider_name = self.models_provider_var.get()
            model_id = self.models_model_var.get()
            if provider_name and model_id and 'agents' in self.config and 'defaults' in self.config['agents']:
                new_model_key = f"{provider_name}/{model_id}"
                # 直接更新主模型
                if 'model' in self.config['agents']['defaults']:
                    self.config['agents']['defaults']['model']['primary'] = new_model_key
                else:
                    self.config['agents']['defaults']['model'] = {'primary': new_model_key}
                # 确保模型列表存在
                if 'models' not in self.config['agents']['defaults']:
                    self.config['agents']['defaults']['models'] = {}
                # 清空模型列表，只保留新模型
                self.config['agents']['defaults']['models'] = {}
                self.config['agents']['defaults']['models'][new_model_key] = {}
            
            # 保存配置文件
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
            
            self.status_var.set(f"已保存: {os.path.basename(self.config_path)}")
            # 自动加载配置
            self.load_config()
        except Exception as e:
            self.status_var.set(f"错误: 保存配置文件失败: {e}")
    
    def init_meta_tab(self):
        """初始化元数据标签页"""
        self.meta_frame = ttk.Frame(self.meta_tab, padding="10")
        self.meta_frame.pack(fill=tk.BOTH, expand=True)
        
        # 创建版本号标签和输入框
        ttk.Label(self.meta_frame, text="版本号:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.meta_version_var = tk.StringVar()
        ttk.Entry(self.meta_frame, textvariable=self.meta_version_var, width=50).grid(row=0, column=1, sticky=tk.W, pady=5)
        
        # 创建最后修改时间标签和输入框
        ttk.Label(self.meta_frame, text="最后修改时间:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.meta_touched_at_var = tk.StringVar()
        ttk.Entry(self.meta_frame, textvariable=self.meta_touched_at_var, width=50).grid(row=1, column=1, sticky=tk.W, pady=5)
    
    def update_meta_tab(self):
        """更新元数据标签页的内容"""
        if not self.config or 'meta' not in self.config:
            return
        
        meta = self.config['meta']
        self.meta_version_var.set(meta.get('lastTouchedVersion', ''))
        self.meta_touched_at_var.set(meta.get('lastTouchedAt', ''))
    
    def get_meta_values(self):
        """获取元数据标签页的值"""
        if not self.config:
            return
        
        if 'meta' not in self.config:
            self.config['meta'] = {}
        
        self.config['meta']['lastTouchedVersion'] = self.meta_version_var.get()
        self.config['meta']['lastTouchedAt'] = self.meta_touched_at_var.get()
    
    def init_models_tab(self):
        """初始化模型配置标签页"""
        self.models_frame = ttk.Frame(self.models_tab, padding="10")
        self.models_frame.pack(fill=tk.BOTH, expand=True)
        
        # 创建模型模式标签和下拉菜单
        ttk.Label(self.models_frame, text="模型模式:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.models_mode_var = tk.StringVar()
        mode_combobox = ttk.Combobox(self.models_frame, textvariable=self.models_mode_var, width=47)
        mode_combobox['values'] = ('merge', 'local', 'remote')
        mode_combobox.grid(row=0, column=1, sticky=tk.W, pady=5)
        
        # 创建提供者名称标签和输入框
        ttk.Label(self.models_frame, text="提供者名称:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.models_provider_var = tk.StringVar()
        ttk.Entry(self.models_frame, textvariable=self.models_provider_var, width=50).grid(row=1, column=1, sticky=tk.W, pady=5)
        
        # 创建baseUrl标签和输入框
        ttk.Label(self.models_frame, text="baseUrl:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.models_baseurl_var = tk.StringVar()
        ttk.Entry(self.models_frame, textvariable=self.models_baseurl_var, width=50).grid(row=2, column=1, sticky=tk.W, pady=5)
        # 添加提示文本（下一行）
        ttk.Label(self.models_frame, text="(请去往相应模型厂商获取)", font=("Arial", 8), foreground="#666").grid(row=3, column=1, sticky=tk.W, pady=2)
        
        # 创建apiKey标签和输入框
        ttk.Label(self.models_frame, text="apiKey:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.models_apikey_var = tk.StringVar()
        ttk.Entry(self.models_frame, textvariable=self.models_apikey_var, width=50).grid(row=4, column=1, sticky=tk.W, pady=5)
        # 添加提示文本（下一行）
        ttk.Label(self.models_frame, text="(请去往相应模型厂商获取)", font=("Arial", 8), foreground="#666").grid(row=5, column=1, sticky=tk.W, pady=2)
        
        # 创建模型ID标签和下拉菜单
        ttk.Label(self.models_frame, text="模型ID:").grid(row=6, column=0, sticky=tk.W, pady=5)
        self.models_model_var = tk.StringVar()
        self.models_model_combobox = ttk.Combobox(self.models_frame, textvariable=self.models_model_var, width=47)
        self.models_model_combobox.grid(row=6, column=1, sticky=tk.W, pady=5)
        
        # 创建获取模型按钮
        self.get_models_btn = ttk.Button(self.models_frame, text="获取模型列表", command=self.get_models)
        self.get_models_btn.grid(row=7, column=1, sticky=tk.W, pady=5)
        
        # 创建模型参数标签和输入框
        ttk.Label(self.models_frame, text="模型名称:").grid(row=8, column=0, sticky=tk.W, pady=5)
        self.models_model_name_var = tk.StringVar()
        ttk.Entry(self.models_frame, textvariable=self.models_model_name_var, width=50).grid(row=8, column=1, sticky=tk.W, pady=5)
        
        ttk.Label(self.models_frame, text="推理功能:").grid(row=9, column=0, sticky=tk.W, pady=5)
        self.models_model_reasoning_var = tk.BooleanVar()
        checkbutton = ttk.Checkbutton(self.models_frame, variable=self.models_model_reasoning_var)
        checkbutton.grid(row=9, column=1, sticky=tk.W, pady=5)
        # 添加提示文本
        ttk.Label(self.models_frame, text="(启用后模型会提供详细推理过程，禁用后直接给出答案。注意：启用推理会增加额外的token使用量和响应时间)", font=("Arial", 8), foreground="#666").grid(row=9, column=1, sticky=tk.W, padx=30, pady=5)
        
        ttk.Label(self.models_frame, text="上下文窗口:").grid(row=10, column=0, sticky=tk.W, pady=5)
        self.models_model_context_window_var = tk.StringVar()
        ttk.Entry(self.models_frame, textvariable=self.models_model_context_window_var, width=50).grid(row=10, column=1, sticky=tk.W, pady=5)
        
        ttk.Label(self.models_frame, text="最大 tokens:").grid(row=11, column=0, sticky=tk.W, pady=5)
        self.models_model_max_tokens_var = tk.StringVar()
        ttk.Entry(self.models_frame, textvariable=self.models_model_max_tokens_var, width=50).grid(row=11, column=1, sticky=tk.W, pady=5)
    
    def update_models_tab(self):
        """更新模型配置标签页的内容"""
        if not self.config or 'models' not in self.config:
            return
        
        models = self.config['models']
        self.models_mode_var.set(models.get('mode', 'merge'))
        
        # 获取第一个提供者的信息
        if 'providers' in models and models['providers']:
            provider_name = next(iter(models['providers']))
            provider = models['providers'][provider_name]
            self.models_provider_var.set(provider_name)
            self.models_baseurl_var.set(provider.get('baseUrl', ''))
            self.models_apikey_var.set(provider.get('apiKey', ''))
            
            # 更新模型下拉菜单
            if 'models' in provider:
                model_ids = [model['id'] for model in provider['models']]
                self.models_model_combobox['values'] = model_ids
                if model_ids:
                    self.models_model_var.set(model_ids[0])
                    # 更新模型参数
                    self.update_model_params(provider_name, model_ids[0])
                else:
                    self.models_model_var.set('')
                    # 清空模型参数
                    self.clear_model_params()
            else:
                self.models_model_combobox['values'] = []
                self.models_model_var.set('')
                # 清空模型参数
                self.clear_model_params()
        else:
            self.models_provider_var.set('')
            self.models_baseurl_var.set('')
            self.models_apikey_var.set('')
            self.models_model_combobox['values'] = []
            self.models_model_var.set('')
            # 清空模型参数
            self.clear_model_params()
    
    def update_model_params(self, provider_name, model_id):
        """更新模型参数"""
        if not self.config or 'models' not in self.config:
            return
        
        models = self.config['models']
        if 'providers' in models and provider_name in models['providers']:
            provider = models['providers'][provider_name]
            if 'models' in provider:
                for model in provider['models']:
                    if model['id'] == model_id:
                        self.models_model_name_var.set(model.get('name', ''))
                        self.models_model_reasoning_var.set(model.get('reasoning', False))
                        self.models_model_context_window_var.set(str(model.get('contextWindow', 64000)))
                        self.models_model_max_tokens_var.set(str(model.get('maxTokens', 4096)))
                        return
        
        # 如果找不到模型，清空参数
        self.clear_model_params()
    
    def clear_model_params(self):
        """清空模型参数"""
        self.models_model_name_var.set('')
        self.models_model_reasoning_var.set(False)
        self.models_model_context_window_var.set('64000')
        self.models_model_max_tokens_var.set('4096')
    
    def get_models(self):
        """从API获取模型列表"""
        import requests
        
        base_url = self.models_baseurl_var.get()
        api_key = self.models_apikey_var.get()
        
        if not base_url or not api_key:
            messagebox.showerror("错误", "请先填写baseUrl和apiKey")
            return
        
        try:
            # 尝试调用OpenAI兼容的API获取模型列表
            headers = {
                'Authorization': f'Bearer {api_key}',
                'Content-Type': 'application/json'
            }
            response = requests.get(f'{base_url}/v1/models', headers=headers, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                models = [model['id'] for model in data.get('data', [])]
                if models:
                    self.models_model_combobox['values'] = models
                    self.models_model_var.set(models[0])
                    # 更新模型参数
                    provider_name = self.models_provider_var.get()
                    if provider_name and self.config and 'models' in self.config:
                        # 直接修改现有模型的ID
                        if 'providers' in self.config['models'] and provider_name in self.config['models']['providers']:
                            provider = self.config['models']['providers'][provider_name]
                            if 'models' in provider and provider['models']:
                                # 获取旧的模型ID
                                old_model_id = provider['models'][0]['id']
                                # 修改第一个模型的ID
                                provider['models'][0]['id'] = models[0]
                                provider['models'][0]['name'] = models[0] + " (Custom Provider)"
                                # 更新代理配置中的模型引用
                                if 'agents' in self.config and 'defaults' in self.config['agents']:
                                    old_model_key = f"{provider_name}/{old_model_id}"
                                    new_model_key = f"{provider_name}/{models[0]}"
                                    # 无论主模型是否使用的是旧模型，都更新为新模型
                                    if 'model' in self.config['agents']['defaults']:
                                        self.config['agents']['defaults']['model']['primary'] = new_model_key
                                    # 更新模型列表
                                    if 'models' in self.config['agents']['defaults']:
                                        if old_model_key in self.config['agents']['defaults']['models']:
                                            del self.config['agents']['defaults']['models'][old_model_key]
                                        if new_model_key not in self.config['agents']['defaults']['models']:
                                            self.config['agents']['defaults']['models'][new_model_key] = {}
                    messagebox.showinfo("成功", f"获取到 {len(models)} 个模型")
                else:
                    messagebox.showinfo("信息", "未获取到模型")
            else:
                messagebox.showerror("错误", f"获取模型失败: {response.status_code}")
        except Exception as e:
            messagebox.showerror("错误", f"请求失败: {str(e)}")
    
    def get_models_values(self):
        """获取模型配置标签页的值"""
        if not self.config:
            return
        
        if 'models' not in self.config:
            self.config['models'] = {}
        
        self.config['models']['mode'] = self.models_mode_var.get()
        
        # 更新提供者信息
        provider_name = self.models_provider_var.get()
        if provider_name:
            if 'providers' not in self.config['models']:
                self.config['models']['providers'] = {}
            
            # 检查是否存在旧的提供者
            old_provider_name = None
            old_model_id = None
            
            # 查找是否有其他提供者
            if 'providers' in self.config['models'] and self.config['models']['providers']:
                # 获取第一个提供者的名称和模型ID
                for key in self.config['models']['providers']:
                    old_provider_name = key
                    old_provider_data = self.config['models']['providers'][key]
                    if 'models' in old_provider_data and old_provider_data['models']:
                        old_model_id = old_provider_data['models'][0]['id']
                    break
            
            # 获取或创建新的提供者
            provider = self.config['models']['providers'].get(provider_name, {})
            
            # 保存新的提供者
            self.config['models']['providers'][provider_name] = provider
            
            # 如果存在旧的提供者且名称不同，删除旧的提供者
            if old_provider_name and old_provider_name != provider_name:
                del self.config['models']['providers'][old_provider_name]
            
            provider['baseUrl'] = self.models_baseurl_var.get()
            provider['apiKey'] = self.models_apikey_var.get()
            
            # 更新api字段
            if 'api' not in provider:
                provider['api'] = 'openai-completions'
            
            # 更新模型参数
            model_id = self.models_model_var.get()
            if model_id:
                if 'models' not in provider:
                    provider['models'] = []
                
                # 确保至少有一个模型
                if not provider['models']:
                    provider['models'].append({
                        "id": model_id,
                        "name": self.models_model_name_var.get() or (model_id + " (Custom Provider)"),
                        "reasoning": self.models_model_reasoning_var.get(),
                        "input": ["text"],
                        "cost": {
                            "input": 0,
                            "output": 0,
                            "cacheRead": 0,
                            "cacheWrite": 0
                        },
                        "contextWindow": int(self.models_model_context_window_var.get() or 64000),
                        "maxTokens": int(self.models_model_max_tokens_var.get() or 4096)
                    })
                else:
                    # 修改第一个模型的参数
                    model = provider['models'][0]
                    old_model_id = model['id']
                    model['id'] = model_id
                    # 更新模型名称
                    model['name'] = model_id + " (Custom Provider)"
                    model['reasoning'] = self.models_model_reasoning_var.get()
                    model['contextWindow'] = int(self.models_model_context_window_var.get() or 64000)
                    model['maxTokens'] = int(self.models_model_max_tokens_var.get() or 4096)
                
                # 更新代理配置中的模型引用
                if 'agents' in self.config and 'defaults' in self.config['agents']:
                    # 生成新的模型键
                    new_model_key = f"{provider_name}/{model_id}"
                    
                    # 无论主模型是否使用的是旧模型，都更新为新模型
                    if 'model' in self.config['agents']['defaults']:
                        # 直接更新主模型
                        self.config['agents']['defaults']['model']['primary'] = new_model_key
                    else:
                        # 如果没有主模型配置，创建一个
                        self.config['agents']['defaults']['model'] = {'primary': new_model_key}
                    
                    # 确保模型列表存在
                    if 'models' not in self.config['agents']['defaults']:
                        self.config['agents']['defaults']['models'] = {}
                    
                    # 清空模型列表，只保留新模型
                    self.config['agents']['defaults']['models'] = {}
                    self.config['agents']['defaults']['models'][new_model_key] = {}
    
    def init_agents_tab(self):
        """初始化代理配置标签页"""
        self.agents_frame = ttk.Frame(self.agents_tab, padding="10")
        self.agents_frame.pack(fill=tk.BOTH, expand=True)
        

        
        # 创建默认配置部分
        self.agents_default_frame = ttk.LabelFrame(self.agents_frame, text="默认配置", padding="10")
        self.agents_default_frame.pack(fill=tk.X, pady=5)
        
        # 创建主模型标签和输入框
        ttk.Label(self.agents_default_frame, text="主模型:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.agents_primary_var = tk.StringVar()
        ttk.Entry(self.agents_default_frame, textvariable=self.agents_primary_var, width=50).grid(row=0, column=1, sticky=tk.W, pady=5)
        
        # 创建工作目录标签和输入框
        ttk.Label(self.agents_default_frame, text="工作目录:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.agents_workspace_var = tk.StringVar()
        ttk.Entry(self.agents_default_frame, textvariable=self.agents_workspace_var, width=50).grid(row=1, column=1, sticky=tk.W, pady=5)
        
        # 创建最大并发数标签和输入框
        ttk.Label(self.agents_default_frame, text="最大并发数:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.agents_max_concurrent_var = tk.StringVar()
        ttk.Entry(self.agents_default_frame, textvariable=self.agents_max_concurrent_var, width=50).grid(row=2, column=1, sticky=tk.W, pady=5)
        
        # 创建 agents 列表框架
        self.agents_list_frame = ttk.LabelFrame(self.agents_frame, text="代理列表", padding="10")
        self.agents_list_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # 创建 agents 列表
        self.agents_listbox = tk.Listbox(self.agents_list_frame, width=50)
        self.agents_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # 创建滚动条
        scrollbar = ttk.Scrollbar(self.agents_list_frame, orient=tk.VERTICAL, command=self.agents_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.agents_listbox.config(yscrollcommand=scrollbar.set)
        
        # 绑定列表框选择事件
        self.agents_listbox.bind("<<ListboxSelect>>", self.on_listbox_select)
    
    def update_agents_tab(self):
        """更新代理配置标签页的内容"""
        if not self.config or 'agents' not in self.config:
            return
        
        # 清空 agents 列表
        self.agents_listbox.delete(0, tk.END)
        
        # 只显示默认配置
        if 'defaults' in self.config['agents']:
            self.agents_listbox.insert(tk.END, 'defaults')
            
            # 更新默认配置
            defaults = self.config['agents']['defaults']
            self.agents_primary_var.set(defaults['model'].get('primary', ''))
            self.agents_workspace_var.set(defaults.get('workspace', ''))
            self.agents_max_concurrent_var.set(str(defaults.get('maxConcurrent', '')))
    
    def on_listbox_select(self, event):
        """处理列表框选择事件"""
        selection = self.agents_listbox.curselection()
        if not selection:
            return
        
        # 只处理默认配置
        if 'defaults' in self.config['agents']:
            agent_config = self.config['agents']['defaults']
            self.agents_primary_var.set(agent_config['model'].get('primary', ''))
            self.agents_workspace_var.set(agent_config.get('workspace', ''))
            self.agents_max_concurrent_var.set(str(agent_config.get('maxConcurrent', '')))
    
    def refresh_agent_config(self):
        """刷新当前代理的配置"""
        # 重新加载配置文件
        self.load_config()
        # 触发代理选择事件，更新配置显示
        self.on_agent_selected(None)
        # 更新状态显示
        self.status_var.set("配置已刷新")
    
    def get_agents_values(self):
        """获取代理配置标签页的值"""
        if not self.config:
            return
        
        if 'agents' not in self.config:
            self.config['agents'] = {}
        
        # 只保存默认配置
        if 'defaults' not in self.config['agents']:
            self.config['agents']['defaults'] = {}
        if 'model' not in self.config['agents']['defaults']:
            self.config['agents']['defaults']['model'] = {}
        
        agent_config = self.config['agents']['defaults']
        
        # 保存配置值
        agent_config['model']['primary'] = self.agents_primary_var.get()
        agent_config['workspace'] = self.agents_workspace_var.get()
        
        try:
            max_concurrent = int(self.agents_max_concurrent_var.get())
            agent_config['maxConcurrent'] = max_concurrent
        except ValueError:
            pass
    

    
    def init_gateway_tab(self):
        """初始化网关配置标签页"""
        self.gateway_frame = ttk.Frame(self.gateway_tab, padding="10")
        self.gateway_frame.pack(fill=tk.BOTH, expand=True)
        
        # 创建端口标签和输入框
        ttk.Label(self.gateway_frame, text="端口:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.gateway_port_var = tk.StringVar()
        ttk.Entry(self.gateway_frame, textvariable=self.gateway_port_var, width=50).grid(row=0, column=1, sticky=tk.W, pady=5)
        
        # 创建模式标签和输入框
        ttk.Label(self.gateway_frame, text="模式:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.gateway_mode_var = tk.StringVar()
        ttk.Entry(self.gateway_frame, textvariable=self.gateway_mode_var, width=50).grid(row=1, column=1, sticky=tk.W, pady=5)
        
        # 创建绑定地址标签和输入框
        ttk.Label(self.gateway_frame, text="绑定地址:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.gateway_bind_var = tk.StringVar()
        ttk.Entry(self.gateway_frame, textvariable=self.gateway_bind_var, width=50).grid(row=2, column=1, sticky=tk.W, pady=5)
        
        # 创建认证令牌标签和输入框
        ttk.Label(self.gateway_frame, text="认证令牌:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.gateway_token_var = tk.StringVar()
        ttk.Entry(self.gateway_frame, textvariable=self.gateway_token_var, width=50).grid(row=3, column=1, sticky=tk.W, pady=5)
    

    
    def update_gateway_tab(self):
        """更新网关配置标签页的内容"""
        if not self.config or 'gateway' not in self.config:
            return
        
        gateway = self.config['gateway']
        self.gateway_port_var.set(str(gateway.get('port', '')))
        self.gateway_mode_var.set(gateway.get('mode', ''))
        self.gateway_bind_var.set(gateway.get('bind', ''))
        
        if 'auth' in gateway:
            self.gateway_token_var.set(gateway['auth'].get('token', ''))
        else:
            self.gateway_token_var.set('')
    
    def get_gateway_values(self):
        """获取网关配置标签页的值"""
        if not self.config:
            return
        
        if 'gateway' not in self.config:
            self.config['gateway'] = {}
        if 'auth' not in self.config['gateway']:
            self.config['gateway']['auth'] = {}
        
        gateway = self.config['gateway']
        
        try:
            port = int(self.gateway_port_var.get())
            gateway['port'] = port
        except ValueError:
            pass
        
        gateway['mode'] = self.gateway_mode_var.get()
        gateway['bind'] = self.gateway_bind_var.get()
        gateway['auth']['token'] = self.gateway_token_var.get()

if __name__ == "__main__":
    root = tk.Tk()
    app = ConfigGUI(root)
    root.mainloop()
