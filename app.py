#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成AIパスポート試験対策 Webアプリケーション
2026年2月試験〜 新シラバス（第4版）完全対応
"""

from flask import Flask, render_template, request, jsonify, session, abort
import random
import os
import glob
import re
from questions_extra import EXTRA_QUESTIONS
from questions_extra2 import EXTRA_QUESTIONS_3
from questions_extra3 import EXTRA_QUESTIONS_4

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'genai_passport_practice_2026')


class GenAIPassportData:
    def __init__(self):
        self.questions = self._build_questions() + EXTRA_QUESTIONS + EXTRA_QUESTIONS_3 + EXTRA_QUESTIONS_4
        self.chapters = {
            1: "AI（人工知能）",
            2: "生成AI（ジェネレーティブAI）",
            3: "現在の生成AIの動向",
            4: "情報リテラシー・基本理念とAI社会原則",
            5: "テキスト生成AIのプロンプト制作と実例",
        }

    def get_by_chapter(self, chapter):
        return [q for q in self.questions if q["chapter"] == chapter]

    def _build_questions(self):
        return [
            # ===== 第1章 AI（人工知能） =====
            {
                "id": 1, "chapter": 1,
                "question": "「AI（人工知能）」という用語が初めて提唱された会議はどれか。",
                "choices": ["チューリング会議", "ダートマス会議", "シャノン会議", "フォン・ノイマン会議"],
                "answer": 1,
                "explanation": "1956年のダートマス会議でジョン・マッカーシーが「AI」という用語を初めて提唱しました。"
            },
            {
                "id": 2, "chapter": 1,
                "question": "人間がルールを定義せず、データからパターンを自動的に学習する仕組みはどれか。",
                "choices": ["ルールベース", "機械学習", "エキスパートシステム", "探索"],
                "answer": 1,
                "explanation": "機械学習はデータからパターンを自動学習します。ルールベースは人間がif-then形式でルールを定義する手法です。"
            },
            {
                "id": 3, "chapter": 1,
                "question": "正解ラベルなしでデータの構造やグループを発見する学習手法はどれか。",
                "choices": ["教師あり学習", "教師なし学習", "強化学習", "転移学習"],
                "answer": 1,
                "explanation": "教師なし学習はラベルなしデータから構造を発見します。クラスタリングや次元削減が代表例です。"
            },
            {
                "id": 4, "chapter": 1,
                "question": "訓練データに過度に適合し、未知のデータに対する性能が低下する現象を何というか。",
                "choices": ["正則化", "ドロップアウト", "過学習（オーバーフィッティング）", "転移学習"],
                "answer": 2,
                "explanation": "過学習（オーバーフィッティング）は訓練データに適合しすぎて、未知データへの汎化性能が低下する現象です。"
            },
            {
                "id": 5, "chapter": 1,
                "question": "学習時にランダムにノードを無効化して過学習を防ぐ手法はどれか。",
                "choices": ["正則化", "ドロップアウト", "転移学習", "クラスタリング"],
                "answer": 1,
                "explanation": "ドロップアウトは学習時にランダムにノードを無効化して過学習を防ぎます。正則化はモデルの複雑さにペナルティを課す別の手法です。"
            },
            {
                "id": 6, "chapter": 1,
                "question": "現在実用化されているAIはすべてどの分類に該当するか。",
                "choices": ["強いAI（AGI）", "弱いAI（ANI）", "汎用AI", "超知能AI"],
                "answer": 1,
                "explanation": "現在のAIはすべて特定タスクに特化した弱いAI（ANI: Artificial Narrow Intelligence）です。AGIは未実現です。"
            },
            {
                "id": 7, "chapter": 1,
                "question": "第二次AIブームの中心的な技術はどれか。",
                "choices": ["ディープラーニング", "エキスパートシステム", "ビッグデータ", "探索と推論"],
                "answer": 1,
                "explanation": "第二次AIブーム（1980年代）はエキスパートシステムが中心。第一次は探索・推論、第三次はディープラーニング・ビッグデータです。"
            },
            {
                "id": 8, "chapter": 1,
                "question": "「2045年にAIが人間の知能を超える」と予測した人物は誰か。",
                "choices": ["ヴァーナー・ヴィンジ", "ジョン・マッカーシー", "レイ・カーツワイル", "アラン・チューリング"],
                "answer": 2,
                "explanation": "レイ・カーツワイルが2045年にシンギュラリティが到来すると予測しました（2045年問題）。ヴィンジはシンギュラリティ概念の提唱者です。"
            },
            {
                "id": 9, "chapter": 1,
                "question": "AIが実現した技術を「それはAIではない」と過小評価する心理現象を何というか。",
                "choices": ["シンギュラリティ", "AI効果", "ハルシネーション", "アライメント"],
                "answer": 1,
                "explanation": "AI効果は、AIが実現した技術を「それはAIではない」と過小評価する心理現象です。"
            },
            {
                "id": 10, "chapter": 1,
                "question": "学習済みモデルの知識を別のタスクに再利用する手法はどれか。",
                "choices": ["ファインチューニング", "転移学習", "ドロップアウト", "正則化"],
                "answer": 1,
                "explanation": "転移学習は学習済みモデルの知識を別タスクに再利用する手法です。ファインチューニングは特定タスク向けの追加学習です。"
            },
            {
                "id": 11, "chapter": 1,
                "question": "「あらゆる問題に万能なアルゴリズムは存在しない」という定理はどれか。",
                "choices": ["ムーアの法則", "ノーフリーランチ定理", "ベイズの定理", "大数の法則"],
                "answer": 1,
                "explanation": "ノーフリーランチ定理は「あらゆる問題に対して最適な単一のアルゴリズムは存在しない」という定理です。"
            },
            {
                "id": 12, "chapter": 1,
                "question": "ディープラーニングの説明として最も適切なものはどれか。",
                "choices": [
                    "ルールを人間が定義する手法",
                    "多数の層を持つニューラルネットワークによる学習",
                    "少量のデータで学習する手法",
                    "教師なし学習の別名"
                ],
                "answer": 1,
                "explanation": "ディープラーニング（深層学習）は多数の層を持つニューラルネットワークによる学習手法です。"
            },
            {
                "id": 13, "chapter": 1,
                "question": "試行錯誤で報酬を最大化する行動を学習する手法はどれか。",
                "choices": ["教師あり学習", "教師なし学習", "強化学習", "半教師あり学習"],
                "answer": 2,
                "explanation": "強化学習は、エージェントが環境と相互作用しながら試行錯誤で報酬を最大化する行動を学習する手法です。"
            },
            {
                "id": 14, "chapter": 1,
                "question": "少量のラベル付きデータと大量のラベルなしデータを組み合わせて学習する手法はどれか。",
                "choices": ["教師あり学習", "教師なし学習", "強化学習", "半教師あり学習"],
                "answer": 3,
                "explanation": "半教師あり学習は、少量のラベル付きデータと大量のラベルなしデータを組み合わせて学習する手法です。"
            },
            {
                "id": 15, "chapter": 1,
                "question": "データの中から学習に有用な情報を抽出したものを何というか。",
                "choices": ["パラメータ", "特徴量", "ハイパーパラメータ", "データセット"],
                "answer": 1,
                "explanation": "特徴量はデータから学習に有用な情報を抽出したものです。ディープラーニングでは特徴量を自動抽出できる点が革新的です。"
            },

            # ===== 第2章 生成AI（ジェネレーティブAI） =====
            {
                "id": 16, "chapter": 2,
                "question": "生成器と識別器が競い合って学習する生成モデルはどれか。",
                "choices": ["VAE", "GAN", "RNN", "CNN"],
                "answer": 1,
                "explanation": "GAN（敵対的生成ネットワーク）は生成器と識別器が敵対的に学習するモデルです。"
            },
            {
                "id": 17, "chapter": 2,
                "question": "時系列データ（シーケンスデータ）の処理に適したモデルはどれか。",
                "choices": ["CNN", "VAE", "RNN", "GAN"],
                "answer": 2,
                "explanation": "RNN（回帰型ニューラルネットワーク）は隠れ層・リカレント層で過去の情報を保持し、シーケンスデータに対応します。"
            },
            {
                "id": 18, "chapter": 2,
                "question": "Transformerモデルの中核的な仕組みで、入力の各要素間の関連度を計算するものはどれか。",
                "choices": ["畳み込み", "自己注意力（Self-Attention）", "リカレント層", "潜在ベクトル"],
                "answer": 1,
                "explanation": "Self-Attention（自己注意力）は文中の各要素が他の全要素との関係を同時に計算する仕組みで、Transformerの中核技術です。"
            },
            {
                "id": 19, "chapter": 2,
                "question": "BERTの学習手法で、文中の一部を隠して予測させるものはどれか。",
                "choices": ["NSP（Next Sentence Prediction）", "MLM（Masked Language Model）", "RLHF", "Few-Shot Learning"],
                "answer": 1,
                "explanation": "MLM（Masked Language Model）は文中の一部を隠して予測させるBERTの学習手法です。NSPは2文の連続性を予測します。"
            },
            {
                "id": 20, "chapter": 2,
                "question": "人間のフィードバックを用いた強化学習の略称はどれか。",
                "choices": ["NLP", "MLM", "RLHF", "RAG"],
                "answer": 2,
                "explanation": "RLHF（Reinforcement Learning from Human Feedback）は人間のフィードバックを用いた強化学習です。"
            },
            {
                "id": 21, "chapter": 2,
                "question": "AIがもっともらしいが事実と異なる情報を生成する現象を何というか。",
                "choices": ["アライメント", "ファインチューニング", "ハルシネーション", "ディープフェイク"],
                "answer": 2,
                "explanation": "ハルシネーション（Hallucination）はAIがもっともらしいが事実と異なる情報を生成する現象です。"
            },
            {
                "id": 22, "chapter": 2,
                "question": "OpenAIの動画生成AIの名称はどれか。",
                "choices": ["Codex", "Operator", "GPTs", "Sora"],
                "answer": 3,
                "explanation": "SoraはOpenAIの動画生成AIです。Codexはコード生成、OperatorはWebブラウザ操作、GPTsはカスタムChatGPT作成機能です。"
            },
            {
                "id": 23, "chapter": 2,
                "question": "ユーザーがカスタムChatGPTを作成できる機能はどれか。",
                "choices": ["Code Interpreter", "GPTs", "Operator", "Image Generation"],
                "answer": 1,
                "explanation": "GPTsはユーザーがカスタムChatGPTを作成できる機能です。"
            },
            {
                "id": 24, "chapter": 2,
                "question": "Claudeの開発元はどこか。",
                "choices": ["OpenAI", "Google", "Microsoft", "Anthropic"],
                "answer": 3,
                "explanation": "ClaudeはAnthropic社が開発した生成AIです。Gemini=Google、Copilot=Microsoftです。"
            },
            {
                "id": 25, "chapter": 2,
                "question": "AIの出力を人間の意図や価値観に合わせることを何というか。",
                "choices": ["ファインチューニング", "アライメント", "プレトレーニング", "ハルシネーション"],
                "answer": 1,
                "explanation": "アライメント（Alignment）はAIの出力を人間の意図や価値観に合わせることです。"
            },
            {
                "id": 26, "chapter": 2,
                "question": "VAE（変分自己符号化器）でデータを圧縮する部分を何というか。",
                "choices": ["デコーダ", "生成器", "エンコーダ", "識別器"],
                "answer": 2,
                "explanation": "エンコーダはデータを潜在ベクトルに圧縮する部分です。デコーダは潜在ベクトルからデータを復元します。"
            },
            {
                "id": 27, "chapter": 2,
                "question": "AIが自律的にWebブラウザを操作するOpenAIのサービスはどれか。",
                "choices": ["Sora", "Codex", "Operator", "GPTs"],
                "answer": 2,
                "explanation": "OperatorはAIが自律的にWebブラウザを操作するOpenAIのエージェントサービスです。"
            },
            {
                "id": 28, "chapter": 2,
                "question": "画像認識に強く、畳み込み処理で特徴を抽出するモデルはどれか。",
                "choices": ["RNN", "LSTM", "CNN", "GAN"],
                "answer": 2,
                "explanation": "CNN（畳み込みニューラルネットワーク）は畳み込み処理で画像の特徴を抽出するモデルです。"
            },
            {
                "id": 29, "chapter": 2,
                "question": "GPTモデルとBERTモデルの違いとして正しいものはどれか。",
                "choices": [
                    "GPTはエンコーダのみ、BERTはデコーダのみ使用",
                    "GPTはデコーダのみ、BERTはエンコーダのみ使用",
                    "両方ともエンコーダ・デコーダの両方を使用",
                    "GPTは画像生成、BERTはテキスト生成に特化"
                ],
                "answer": 1,
                "explanation": "GPTはデコーダのみ使用しテキスト生成に特化、BERTはエンコーダのみ使用し文脈理解に特化しています。"
            },
            {
                "id": 30, "chapter": 2,
                "question": "RNNの長期依存性問題を解決したモデルはどれか。",
                "choices": ["CNN", "GAN", "LSTM", "VAE"],
                "answer": 2,
                "explanation": "LSTM（長・短期記憶）はRNNの長期依存性問題を解決し、長い文脈を記憶できるモデルです。"
            },
            {
                "id": 31, "chapter": 2,
                "question": "Transformerで単語の順序情報を付与する仕組みを何というか。",
                "choices": ["Self-Attention", "位置エンコーディング", "Attention Mechanism", "畳み込み"],
                "answer": 1,
                "explanation": "位置エンコーディングはTransformerで単語の順序情報を付与する仕組みです。RNNと違い並列処理が可能になります。"
            },
            {
                "id": 32, "chapter": 2,
                "question": "学習済みモデルを特定タスク向けに追加学習することを何というか。",
                "choices": ["プレトレーニング", "ファインチューニング", "転移学習", "強化学習"],
                "answer": 1,
                "explanation": "ファインチューニングは学習済みモデルを特定タスク向けに追加学習することです。プレトレーニングは大量データでの事前学習です。"
            },
            {
                "id": 33, "chapter": 2,
                "question": "Geminiの開発元はどこか。",
                "choices": ["OpenAI", "Google", "Anthropic", "Microsoft"],
                "answer": 1,
                "explanation": "GeminiはGoogleが開発したマルチモーダル対応の生成AIです。"
            },
            {
                "id": 34, "chapter": 2,
                "question": "BERTを軽量化したモデルの名称はどれか。",
                "choices": ["RoBERTa", "ALBERT", "GPT-2", "InstructGPT"],
                "answer": 1,
                "explanation": "ALBERT（a Lite BERT）はBERTを軽量化したモデルです。RoBERTaはBERTの学習手法を改良したモデルです。"
            },

            # ===== 第3章 現在の生成AIの動向 =====
            {
                "id": 35, "chapter": 3,
                "question": "回転・反転等でデータ量を人工的に増やす手法を何というか。",
                "choices": ["正規化", "リマスタリング", "データの水増し（augmentation）", "マスキング"],
                "answer": 2,
                "explanation": "データの水増し（augmentation）は回転・反転等でデータ量を人工的に増やす手法です。"
            },
            {
                "id": 36, "chapter": 3,
                "question": "ディープラーニングを使って実在の人物の顔や声を精巧に偽造する技術を何というか。",
                "choices": ["ハルシネーション", "ディープフェイク", "ソーシャルエンジニアリング", "フィッシング"],
                "answer": 1,
                "explanation": "ディープフェイク（深層偽造）技術はディープラーニングで人物の顔や声を精巧に偽造する技術です。"
            },
            {
                "id": 37, "chapter": 3,
                "question": "意図的に作られた虚偽情報を何というか。",
                "choices": ["ミスインフォメーション", "ディスインフォメーション", "プロパガンダ", "フェイクニュース"],
                "answer": 1,
                "explanation": "ディスインフォメーション（偽情報）は意図的に作られた虚偽情報です。ミスインフォメーションは意図せず広まった誤情報です。"
            },
            {
                "id": 38, "chapter": 3,
                "question": "RAGの正式名称はどれか。",
                "choices": [
                    "Reinforcement Augmented Generation",
                    "Retrieval-Augmented Generation",
                    "Recursive Attention Generation",
                    "Real-time AI Generation"
                ],
                "answer": 1,
                "explanation": "RAG = Retrieval-Augmented Generation（検索拡張生成）。外部知識を検索しLLMの生成に組み合わせる手法です。"
            },
            {
                "id": 39, "chapter": 3,
                "question": "RAGにおいて、文書を検索しやすい小さな単位に分割したものを何というか。",
                "choices": ["トークン", "ベクトル", "チャンク", "ノード"],
                "answer": 2,
                "explanation": "チャンクは文書を検索しやすい小さな単位に分割したものです。RAGではチャンク化した文書をベクトルDBに格納します。"
            },
            {
                "id": 40, "chapter": 3,
                "question": "テキストを数値ベクトルに変換して格納・検索するデータベースを何というか。",
                "choices": ["リレーショナルデータベース", "グラフデータベース", "ベクトルデータベース", "ドキュメントデータベース"],
                "answer": 2,
                "explanation": "ベクトルデータベースはテキストを数値ベクトルに変換して格納・検索するDBです。RAGの検索基盤として使われます。"
            },
            {
                "id": 41, "chapter": 3,
                "question": "AIモデルが外部ツールやデータソースと連携するための標準プロトコルはどれか。",
                "choices": ["API", "MCP", "HTTP", "RAG"],
                "answer": 1,
                "explanation": "MCP（Model Context Protocol）はAIモデルが外部ツールやデータソースと安全に連携するための標準プロトコルです。"
            },
            {
                "id": 42, "chapter": 3,
                "question": "Googleの動画生成AIはどれか。",
                "choices": ["Sora", "Veo3", "Manus", "GenSpark"],
                "answer": 1,
                "explanation": "Veo3はGoogleの動画生成AIです。SoraはOpenAIの動画生成AIです。"
            },
            {
                "id": 43, "chapter": 3,
                "question": "AIエージェントの特徴として最も適切なものはどれか。",
                "choices": [
                    "人間が逐一指示を出す必要がある",
                    "テキスト生成のみに特化している",
                    "自律的に目標を設定し、ツールを使って行動できる",
                    "オフラインでのみ動作する"
                ],
                "answer": 2,
                "explanation": "AIエージェントは自律的に目標を設定し、計画を立て、ツールを使って行動できるAIシステムです。"
            },
            {
                "id": 44, "chapter": 3,
                "question": "RAGのメリットとして不適切なものはどれか。",
                "choices": [
                    "最新情報を反映できる",
                    "ハルシネーションを完全に排除できる",
                    "社内文書など独自データを活用できる",
                    "モデルの再学習が不要"
                ],
                "answer": 1,
                "explanation": "RAGはハルシネーションを「低減」しますが「完全に排除」はできません。他の3つはRAGの正しいメリットです。"
            },
            {
                "id": 45, "chapter": 3,
                "question": "GenSparkの説明として最も適切なものはどれか。",
                "choices": ["動画生成AI", "AI検索エージェント", "コード生成AI", "音声生成AI"],
                "answer": 1,
                "explanation": "GenSparkはAI検索エージェントです。ManusやSkywork AIもAIエージェントの代表例です。"
            },
            {
                "id": 46, "chapter": 3,
                "question": "過去のデータから次のデータを順番に予測するモデルを何というか。",
                "choices": ["GAN", "自己回帰モデル", "VAE", "CNN"],
                "answer": 1,
                "explanation": "自己回帰モデルは過去のデータから次のデータを順番に予測するモデルで、動画生成にも使われます。"
            },
            {
                "id": 47, "chapter": 3,
                "question": "データの値を一定の範囲（0〜1等）に変換する前処理を何というか。",
                "choices": ["正規化", "データの水増し", "リマスタリング", "マスキング"],
                "answer": 0,
                "explanation": "正規化はデータの値を一定の範囲に変換する前処理です。モデルの学習を安定させる効果があります。"
            },
            {
                "id": 48, "chapter": 3,
                "question": "既存コンテンツの品質を向上させる処理を何というか。",
                "choices": ["正規化", "データの水増し", "リマスタリング", "チャンク化"],
                "answer": 2,
                "explanation": "リマスタリングは既存コンテンツの品質を向上させる処理です。"
            },

            # ===== 第4章 情報リテラシー・基本理念とAI社会原則 =====
            {
                "id": 49, "chapter": 4,
                "question": "SMSを使ったフィッシング詐欺を何というか。",
                "choices": ["ヴィッシング", "スミッシング", "スピアフィッシング", "ベイト攻撃"],
                "answer": 1,
                "explanation": "スミッシング = SMS + フィッシング。ヴィッシング = Voice（音声）+ フィッシングです。"
            },
            {
                "id": 50, "chapter": 4,
                "question": "データを暗号化し身代金を要求するマルウェアはどれか。",
                "choices": ["スパイウェア", "トロイの木馬", "ランサムウェア", "アドウェア"],
                "answer": 2,
                "explanation": "ランサムウェアはデータを暗号化し、復号と引き換えに身代金（ランサム）を要求するマルウェアです。"
            },
            {
                "id": 51, "chapter": 4,
                "question": "偽の口実（身分詐称等）で情報を引き出す手法はどれか。",
                "choices": ["ベイト攻撃", "ブラックメール", "プレテキスト", "スミッシング"],
                "answer": 2,
                "explanation": "プレテキストは偽の口実で情報を引き出すソーシャルエンジニアリング手法です。ベイト攻撃はUSBメモリ等の「餌」で誘導します。"
            },
            {
                "id": 52, "chapter": 4,
                "question": "個人情報保護を監督する独立機関はどれか。",
                "choices": ["総務省", "個人情報保護委員会", "消費者庁", "デジタル庁"],
                "answer": 1,
                "explanation": "個人情報保護委員会は個人情報保護法に基づき設置された独立機関です。"
            },
            {
                "id": 53, "chapter": 4,
                "question": "指紋や顔認証データなど、特定個人を識別できる符号を何というか。",
                "choices": ["要配慮個人情報", "機微情報", "個人識別符号", "匿名加工情報"],
                "answer": 2,
                "explanation": "個人識別符号は指紋、顔認証データ、マイナンバーなど特定個人を識別できる符号です。"
            },
            {
                "id": 54, "chapter": 4,
                "question": "不当な差別・偏見が生じうる情報で、取得に本人同意が必要なものはどれか。",
                "choices": ["個人識別符号", "要配慮個人情報", "匿名加工情報", "機微情報"],
                "answer": 1,
                "explanation": "要配慮個人情報は人種、信条、病歴、犯罪歴など不当な差別・偏見が生じうる情報で、取得に本人同意が必要です。"
            },
            {
                "id": 55, "chapter": 4,
                "question": "特定個人を識別できないよう加工した情報を何というか。",
                "choices": ["要配慮個人情報", "機微情報", "匿名加工情報", "個人識別符号"],
                "answer": 2,
                "explanation": "匿名加工情報は特定個人を識別できないよう加工した情報です。統計データ等に利用されます。"
            },
            {
                "id": 56, "chapter": 4,
                "question": "創作物を保護し、登録不要で自動的に発生する権利はどれか。",
                "choices": ["特許権", "商標権", "著作権", "意匠権"],
                "answer": 2,
                "explanation": "著作権は創作と同時に自動的に発生します。特許権・商標権・意匠権は出願・登録が必要です。"
            },
            {
                "id": 57, "chapter": 4,
                "question": "著名人の氏名・肖像が持つ経済的価値を保護する権利はどれか。",
                "choices": ["肖像権", "パブリシティ権", "著作権", "商標権"],
                "answer": 1,
                "explanation": "パブリシティ権は著名人の氏名・肖像の経済的価値を保護する権利です。肖像権は容姿の無断利用を防ぐ権利です。"
            },
            {
                "id": 58, "chapter": 4,
                "question": "営業秘密の3要件に含まれないものはどれか。",
                "choices": ["秘密管理性", "有用性", "非公知性", "独創性"],
                "answer": 3,
                "explanation": "営業秘密の3要件は秘密管理性・有用性・非公知性です。独創性は要件に含まれません。"
            },
            {
                "id": 59, "chapter": 4,
                "question": "AI社会の基本理念「Diversity & Inclusion」の日本語訳として正しいものはどれか。",
                "choices": [
                    "人間の尊厳が尊重される社会",
                    "多様な背景を持つ人々が多様な幸せを追求できる社会",
                    "持続可能な社会",
                    "安全で公平な社会"
                ],
                "answer": 1,
                "explanation": "Diversity & Inclusion = 多様な背景を持つ人々が多様な幸せを追求できる社会。Dignity = 人間の尊厳、Sustainability = 持続可能な社会です。"
            },
            {
                "id": 60, "chapter": 4,
                "question": "AIサービスを提供する主体を何というか。",
                "choices": ["AI開発者（AI Developer）", "AI提供者（AI Provider）", "AI利用者（AI Business User）", "AIガバナー"],
                "answer": 1,
                "explanation": "AI Provider（AI提供者）はAIサービスを提供する主体です。AI Developer = 開発者、AI Business User = 利用者です。"
            },
            {
                "id": 61, "chapter": 4,
                "question": "2025年6月4日に公布されたAI関連の法律の通称はどれか。",
                "choices": ["AI基本法", "AI規制法", "AI新法", "AI推進法"],
                "answer": 2,
                "explanation": "AI新法（正式名称: 人工知能関連技術の研究開発及び活用の推進に関する法律）は2025年6月4日に公布されました。"
            },
            {
                "id": 62, "chapter": 4,
                "question": "AI社会原則に含まれないものはどれか。",
                "choices": ["透明性", "アカウンタビリティ", "利益最大化", "プライバシー保護"],
                "answer": 2,
                "explanation": "「利益最大化」はAI社会原則に含まれません。原則は人間中心、安全性・公平性、プライバシー保護、セキュリティ確保、透明性、アカウンタビリティです。"
            },
            {
                "id": 63, "chapter": 4,
                "question": "音声通話を使ったフィッシング詐欺を何というか。",
                "choices": ["スミッシング", "ヴィッシング", "スピアフィッシング", "プレテキスト"],
                "answer": 1,
                "explanation": "ヴィッシング = Voice（音声）+ フィッシング。電話を使って個人情報を騙し取る手法です。"
            },
            {
                "id": 64, "chapter": 4,
                "question": "特定の個人・組織を狙った標的型フィッシングを何というか。",
                "choices": ["スミッシング", "ヴィッシング", "スピアフィッシング", "ベイト攻撃"],
                "answer": 2,
                "explanation": "スピアフィッシングは特定の個人・組織を狙った標的型フィッシングです。通常のフィッシングより精巧で危険です。"
            },
            {
                "id": 65, "chapter": 4,
                "question": "USBメモリ等の「餌」を使って誘導するソーシャルエンジニアリング手法はどれか。",
                "choices": ["ベイト攻撃", "ブラックメール", "プレテキスト", "ヴィッシング"],
                "answer": 0,
                "explanation": "ベイト攻撃はUSBメモリ等の「餌（ベイト）」を使って標的を誘導する手法です。"
            },
            {
                "id": 66, "chapter": 4,
                "question": "個人情報の一部を隠す処理を何というか。",
                "choices": ["匿名加工", "マスキング", "正規化", "暗号化"],
                "answer": 1,
                "explanation": "マスキングは個人情報の一部を隠す処理です（例: 名前を「***」に置換）。生成AIへの入力時に重要です。"
            },
            {
                "id": 67, "chapter": 4,
                "question": "AI社会の基本理念は3つあるが、「Sustainability」の日本語訳はどれか。",
                "choices": ["人間の尊厳が尊重される社会", "多様な幸せを追求できる社会", "持続可能な社会", "安全な社会"],
                "answer": 2,
                "explanation": "Sustainability = 持続可能な社会。Dignity = 人間の尊厳、Diversity & Inclusion = 多様な幸せの追求です。"
            },
            {
                "id": 68, "chapter": 4,
                "question": "AIガバナンスの構築に含まれないものはどれか。",
                "choices": ["環境・リスク分析", "AIガバナンス・ゴール", "AIマネジメントシステム", "利益配分計画"],
                "answer": 3,
                "explanation": "AIガバナンスの構築は環境・リスク分析、AIガバナンス・ゴール、AIマネジメントシステムで構成されます。"
            },
            {
                "id": 69, "chapter": 4,
                "question": "不正競争防止法で保護される「営業秘密」の要件として正しい組み合わせはどれか。",
                "choices": [
                    "秘密管理性・有用性・非公知性",
                    "秘密管理性・独創性・非公知性",
                    "有用性・独創性・新規性",
                    "秘密管理性・有用性・新規性"
                ],
                "answer": 0,
                "explanation": "営業秘密の3要件は秘密管理性（秘密として管理）・有用性（事業に有用）・非公知性（公に知られていない）です。"
            },
            {
                "id": 70, "chapter": 4,
                "question": "AI生成物の著作権について正しいものはどれか。",
                "choices": [
                    "AIが自律的に生成した物には常に著作権が発生する",
                    "AI生成物には一切著作権は認められない",
                    "人間の創作的関与がある場合は著作権が認められる可能性がある",
                    "著作権はAIの開発者に自動的に帰属する"
                ],
                "answer": 2,
                "explanation": "AIが自律的に生成した物には原則として著作権は発生しませんが、人間の創作的関与がある場合は認められる可能性があります。"
            },

            # ===== 第5章 テキスト生成AIのプロンプト制作と実例 =====
            {
                "id": 71, "chapter": 5,
                "question": "出力のランダム性を制御するハイパーパラメータはどれか。",
                "choices": ["Top-p", "Temperature", "Learning Rate", "Batch Size"],
                "answer": 1,
                "explanation": "Temperatureは出力のランダム性を制御します。低い値→確定的な出力、高い値→創造的な出力になります。"
            },
            {
                "id": 72, "chapter": 5,
                "question": "例示なしで指示のみ与えるプロンプティング手法はどれか。",
                "choices": ["Few-Shot プロンプティング", "Zero-Shot プロンプティング", "Chain-of-Thought", "Self-Consistency"],
                "answer": 1,
                "explanation": "Zero-Shotプロンプティングは例示なしで指示のみ与える手法です。Few-Shotは例を示してから指示します。"
            },
            {
                "id": 73, "chapter": 5,
                "question": "プロンプトの4要素に含まれないものはどれか。",
                "choices": ["Instruction", "Context", "Temperature", "Output Indicator"],
                "answer": 2,
                "explanation": "プロンプトの4要素はInstruction（指示）、Context（文脈）、Input Data（入力データ）、Output Indicator（出力指示）です。Temperatureはハイパーパラメータです。"
            },
            {
                "id": 74, "chapter": 5,
                "question": "直前のn個の単語から次の単語を予測する古典的な言語モデルはどれか。",
                "choices": ["Transformerモデル", "n-gramモデル", "LLM", "ニューラル言語モデル"],
                "answer": 1,
                "explanation": "n-gramモデルは直前のn個の単語から次の単語を予測する古典的な言語モデルです。"
            },
            {
                "id": 75, "chapter": 5,
                "question": "テキスト生成AIが不得意なこととして不適切なものはどれか。",
                "choices": ["正確な文字数の指定", "文章の要約", "計算", "最新の情報"],
                "answer": 1,
                "explanation": "文章の要約はテキスト生成AIが得意なタスクです。正確な文字数指定、計算、最新情報、芸術の批評は不得意です。"
            },
            {
                "id": 76, "chapter": 5,
                "question": "大量の汎用データでモデルを事前学習することを何というか。",
                "choices": ["ファインチューニング", "プレトレーニング", "転移学習", "強化学習"],
                "answer": 1,
                "explanation": "プレトレーニングは大量の汎用データでの事前学習です。ファインチューニングは特定タスク向けの追加学習です。"
            },
            {
                "id": 77, "chapter": 5,
                "question": "累積確率がp以下の候補から次の単語を選択するパラメータはどれか。",
                "choices": ["Temperature", "Top-p", "Top-k", "Beam Size"],
                "answer": 1,
                "explanation": "Top-pは累積確率がp以下の候補から次の単語を選択するパラメータです。多様性を制御します。"
            },
            {
                "id": 78, "chapter": 5,
                "question": "いくつかの例を示してからAIに指示を与える手法はどれか。",
                "choices": ["Zero-Shot プロンプティング", "Few-Shot プロンプティング", "プレトレーニング", "ファインチューニング"],
                "answer": 1,
                "explanation": "Few-Shotプロンプティングはいくつかの例を示してから指示を与える手法です。"
            },
            {
                "id": 79, "chapter": 5,
                "question": "プロンプトの要素「Output Indicator」の役割はどれか。",
                "choices": [
                    "AIに背景情報を与える",
                    "処理対象のデータを指定する",
                    "出力の形式や条件を指定する",
                    "AIへの命令を記述する"
                ],
                "answer": 2,
                "explanation": "Output Indicatorは出力の形式や条件を指定する要素です。Context=背景情報、Input Data=処理対象、Instruction=命令です。"
            },
            {
                "id": 80, "chapter": 5,
                "question": "テキスト生成AIを使ったビジネス応用として不適切なものはどれか。",
                "choices": [
                    "メールの作成",
                    "アンケートの分析",
                    "法的拘束力のある契約書の自動締結",
                    "ブレインストーミング"
                ],
                "answer": 2,
                "explanation": "法的拘束力のある契約の自動締結はAIの適切な用途ではありません。メール作成、アンケート分析、ブレインストーミングは適切な活用例です。"
            },
        ]


# データの遅延読み込み
exam_data = None

def get_exam_data():
    global exam_data
    if exam_data is None:
        exam_data = GenAIPassportData()
    return exam_data


def _q_by_id(qid):
    """IDから問題を引き当てる"""
    data = get_exam_data()
    for q in data.questions:
        if q['id'] == qid:
            return q
    return None


def _start_exam(question_ids, mode, timer=0):
    """セッションにIDリストだけ保存して試験開始"""
    session['q_ids'] = question_ids
    session['q_idx'] = 0
    session['q_correct'] = 0
    first = _q_by_id(question_ids[0])
    return render_template('exam.html',
                           question=first, question_num=1,
                           total=len(question_ids), mode=mode,
                           timer_seconds=timer)


@app.route('/')
def index():
    data = get_exam_data()
    chapter_counts = {}
    for ch_id, ch_name in data.chapters.items():
        chapter_counts[ch_id] = {"name": ch_name, "count": len(data.get_by_chapter(ch_id))}
    return render_template('index.html', chapters=chapter_counts, total=len(data.questions))


@app.route('/exam')
def exam():
    data = get_exam_data()
    n = request.args.get('n', 10, type=int)
    n = max(1, min(n, len(data.questions)))
    timer = request.args.get('timer', 0, type=int)
    ids = [q['id'] for q in random.sample(data.questions, n)]
    mode_label = {10: "クイック10問", 30: "ハーフ30問", 60: "本番モード60問"}.get(n, f"ランダム{n}問")
    return _start_exam(ids, mode_label, timer)


@app.route('/exam/<int:chapter>')
def exam_chapter(chapter):
    data = get_exam_data()
    pool = data.get_by_chapter(chapter)
    if not pool:
        return "該当する章がありません", 404
    n = request.args.get('n', 10, type=int)
    if n <= 0 or n > len(pool):
        n = len(pool)
    ids = [q['id'] for q in random.sample(pool, n)]
    chapter_name = data.chapters.get(chapter, "")
    return _start_exam(ids, f"第{chapter}章 {chapter_name}")


@app.route('/exam/weak', methods=['POST'])
def exam_weak():
    data = get_exam_data()
    weak_ids = request.json.get('ids', [])
    if not weak_ids:
        return jsonify({'error': '苦手問題がありません'}), 400
    id_set = set(weak_ids)
    pool = [q for q in data.questions if q['id'] in id_set]
    if not pool:
        return jsonify({'error': '該当する問題が見つかりません'}), 404
    random.shuffle(pool)
    ids = [q['id'] for q in pool[:20]]
    session['q_ids'] = ids
    session['q_idx'] = 0
    session['q_correct'] = 0
    return jsonify({'redirect': '/exam/weak/start'})


@app.route('/exam/weak/start')
def exam_weak_start():
    ids = session.get('q_ids', [])
    if not ids:
        return "苦手問題がセットされていません。ホームからやり直してください。", 400
    first = _q_by_id(ids[0])
    return render_template('exam.html',
                           question=first, question_num=1,
                           total=len(ids), mode="苦手克服モード",
                           timer_seconds=0)


@app.route('/submit_answer', methods=['POST'])
def submit_answer():
    req = request.json
    selected = int(req['answer'])

    ids = session.get('q_ids', [])
    idx = session.get('q_idx', 0)
    correct_count = session.get('q_correct', 0)

    if idx >= len(ids):
        return jsonify({'error': 'Invalid'}), 400

    q = _q_by_id(ids[idx])
    is_correct = selected == q['answer']
    if is_correct:
        correct_count += 1
        session['q_correct'] = correct_count

    resp = {
        'correct': is_correct,
        'correct_answer': q['answer'],
        'explanation': q['explanation'],
        'question_id': q['id'],
    }

    session['q_idx'] = idx + 1

    if idx + 1 < len(ids):
        nq = _q_by_id(ids[idx + 1])
        resp['next_question'] = nq
        resp['question_num'] = idx + 2
        resp['has_next'] = True
    else:
        score = (correct_count / len(ids)) * 100
        resp['has_next'] = False
        resp['final_score'] = {
            'correct': correct_count,
            'total': len(ids),
            'percentage': score,
        }

    return jsonify(resp)


@app.route('/scores')
def view_scores():
    return render_template('scores.html')


# ===== 学習教材 =====
DOCS_DIR = os.path.join(os.path.dirname(__file__), 'docs')

def _doc_list():
    """docsフォルダのmdファイル一覧を返す（README除外）"""
    files = sorted(glob.glob(os.path.join(DOCS_DIR, '*.md')))
    result = []
    for f in files:
        name = os.path.basename(f)
        if name == 'README.md':
            continue
        slug = os.path.splitext(name)[0]
        # ファイル名から表示タイトルを生成（先頭の番号_を除去）
        title = re.sub(r'^\d+_', '', slug).replace('_', ' ')
        result.append({'slug': slug, 'title': title, 'filename': name})
    return result


@app.route('/docs')
def docs_index():
    docs = _doc_list()
    return render_template('docs_index.html', docs=docs)


@app.route('/docs/<slug>')
def docs_view(slug):
    docs = _doc_list()
    filepath = os.path.join(DOCS_DIR, slug + '.md')
    if not os.path.isfile(filepath):
        abort(404)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    # 現在のドキュメントのタイトルを取得
    title = slug
    for d in docs:
        if d['slug'] == slug:
            title = d['title']
            break
    return render_template('docs_view.html', content=content, title=title, docs=docs, current_slug=slug)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(debug=False, host='0.0.0.0', port=port, threaded=True)
