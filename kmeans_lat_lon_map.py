# Plot a map with correspondent lat x long coordinates with label "Grupo".
# in this examples the objetive is to catch error's

from sklearn.cluster import KMeans
import numpy as np
from sklearn.cluster import DBSCAN
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder

def old_get_maps():
    for unidade in df.Grupo.str[:3].unique():
        print(f'Analise GRUPOX {unidade}')
        frentes_ = df[df.Grupo.str[:3] == unidade].Grupo.unique()
        print(f'São {len(frentes_)} Frentes, sendo elas:\n{",".join(frentes_)}')
        kmeans = KMeans(
            n_clusters=len(df[df.Grupo.str[:3] == unidade].Grupo.unique()), init='random',
            n_init=10, max_iter=300, 
            tol=1e-04, random_state=0)
        ta = np.column_stack((df[df.Grupo.str[:3] == unidade].Latitude.values, df[df.Grupo.str[:3] == unidade].Longitude.values))
        predict = kmeans.fit_predict(ta)
        # Plot KMEANS
        '''plt.grid()
        for centroid in range(len(df[df.Grupo.str[:3] == unidade].Grupo.unique())):
            plt.scatter(
                ta[predict == centroid, 0], ta[predict == centroid, 1],
                s=50, #c='purple',
                marker='s', edgecolor='black',
                label=f'CL.{centroid+1} ({len(ta[predict == centroid, 0])} Frotas)'
            )
        plt.scatter(
            kmeans.cluster_centers_[:, 0], kmeans.cluster_centers_[:, 1],
            s=60, marker='*',
            c='red', edgecolor='black',
            label='Centroids')
        plt.legend(scatterpoints=1)
        plt.suptitle(f"Unidade: {unidade}")
        plt.title(f"Frentes: {', '.join(df[df.Grupo.str[:3] == unidade].Grupo.unique())}", size=8)
        plt.xticks(size=7)
        plt.yticks(size=7)
        plt.ylabel('Latitude', size=9)
        plt.xlabel('Longitude', size=9)
        plt.show()'''

        #DBSCAN
        DBSCAN_cluster = DBSCAN(eps=0.01, min_samples=1).fit(ta)
        print(f'DBSCAN - {len(set(DBSCAN_cluster.labels_))} Clusters')
        for id,idx in zip(range(len(df[df.Grupo.str[:3] == unidade].index.values)), df[df.Grupo.str[:3] == unidade].index.values):
            df.loc[idx, 'Cluster'] = predict[id]+1
            df.loc[idx, 'DBSCAN'] = DBSCAN_cluster.labels_[id]+1
        for cluster in df[(df.Grupo.str[:3] == unidade)].DBSCAN.unique():
            slice_ = df[(df.Grupo.str[:3] == unidade) & (df.DBSCAN == cluster)][['Equipamento','Data/Hora','Grupo','Cluster','DBSCAN']]
            print(f'Cluster {cluster} com {len(slice_)} frotas')
            for frente_existente in slice_.Grupo.unique():
                print(f'  - {len(slice_[slice_.Grupo == frente_existente])} frotas da frente {frente_existente}.')

        plt.grid()
        for centroid in range(len(df[df.Grupo.str[:3] == unidade].DBSCAN.unique())):
            plt.scatter(
                ta[predict == centroid, 0], ta[predict == centroid, 1],
                s=50, #c='purple',
                marker='s', edgecolor='black',
                label=f'CL.{centroid+1} ({len(ta[predict == centroid, 0])} Frotas)'
            )
        plt.scatter(
            kmeans.cluster_centers_[:, 0], kmeans.cluster_centers_[:, 1],
            s=60, marker='*',
            c='red', edgecolor='black',
            label='Centroids')
        plt.legend(scatterpoints=1)
        plt.suptitle(f"Unidade: {unidade}")
        plt.title(f"Frentes: {', '.join(df[df.Grupo.str[:3] == unidade].Grupo.unique())}", size=8)
        plt.xticks(size=7)
        plt.yticks(size=7)
        plt.ylabel('Latitude', size=9)
        plt.xlabel('Longitude', size=9)
        plt.show()

        display(df[df.Grupo.str[:3] == unidade][['Equipamento','Data/Hora','Grupo','Cluster','DBSCAN']].sort_values(by=["Cluster"]))
        print('\n\n')

def get_maps():
    for unidade in df.Grupo.str[:3].unique():
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))
        fig.suptitle(f"Unidade: {unidade}")
        lat_lon = np.column_stack((df[df.Grupo.str[:3] == unidade].Latitude.values, df[df.Grupo.str[:3] == unidade].Longitude.values))
        # Aplicando o algoritmo DBSCAN
        DBSCAN_cluster = DBSCAN(eps=0.025, min_samples=2).fit(lat_lon)
        # Grafico Cluster
        scatter1 = ax1.scatter(lat_lon[:,0], lat_lon[:,1], c=DBSCAN_cluster.labels_, cmap='turbo')
        ax1.grid()
        ax1.set_title('Agrupamentos Frotas')
        ax1.set_xlabel('Longitude', size=9)
        ax1.set_ylabel('Latitude', size=9)
        ax1.tick_params(labelsize=7)
        objs1, labels1 = scatter1.legend_elements()
        if np.min(list([int(f.split('{')[1].split('}')[0].replace('−', '-')) for f in labels1])) == -1: labels1_ = [f"Grupo {c+2}: {len(DBSCAN_cluster.labels_[DBSCAN_cluster.labels_ == c])} Frotas" for c in list([int(f.split('{')[1].split('}')[0].replace('−', '-')) for f in labels1])]
        else: labels1_ = [f"Grupo {c+1}: {len(DBSCAN_cluster.labels_[DBSCAN_cluster.labels_ == c])} Frotas" for c in list([int(f.split('{')[1].split('}')[0].replace('−', '-')) for f in labels1])]
        legend1 = ax1.legend(objs1, labels1_, title="Grupo", framealpha=0.3, fontsize=7)
        ax1.add_artist(legend1)
        # Gráfico Frentes
        encoder = LabelEncoder()
        labels = encoder.fit_transform(df[df.Grupo.str[:3] == unidade].Grupo.values)
        scatter2 = ax2.scatter(df[df.Grupo.str[:3] == unidade].Latitude.values, df[df.Grupo.str[:3] == unidade].Longitude.values, c=labels, cmap='rainbow')
        ax2.grid()
        ax2.set_title('Cadastro Frentes')
        ax2.set_xlabel('Longitude', size=9)
        ax2.set_ylabel('Latitude', size=9)
        ax2.tick_params(labelsize=7)
        objs2, labels2 = scatter2.legend_elements()
        labels2_ = [f"{f[-3:]}: {len(df[df.Grupo == f])} Frotas" for f in encoder.classes_]
        legend2 = ax2.legend(objs2, labels2_, title="Frentes", framealpha=0.3, fontsize=7)
        ax2.add_artist(legend2)
        # Plotando
        plt.show()
        print('\n\n')
    
get_maps()
