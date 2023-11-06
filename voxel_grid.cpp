#include <iostream>
#include <fstream>
#include <vector>
#include <pcl/point_types.h>
#include <pcl/point_cloud.h>
#include <pcl/filters/voxel_grid.h>
#include <pcl/visualization/pcl_visualizer.h>

int main() {
    std::ifstream inFile("roadpoints.txt");
    pcl::PointCloud<pcl::PointXYZ>::Ptr cloud(new pcl::PointCloud<pcl::PointXYZ>);

    if (inFile.is_open()) {
        float x, y, z;
        while (inFile >> x >> y >> z) {
            cloud->points.push_back(pcl::PointXYZ(x, y, z));
        }
        inFile.close();
    } else {
        std::cerr << "Unable to open file";
        return 1;
    }

    // Continue from the previous code...

    cloud->width = cloud->points.size();
    cloud->height = 1;
    cloud->is_dense = false;

    pcl::VoxelGrid<pcl::PointXYZ> voxelGrid;
    voxelGrid.setInputCloud(cloud);
    voxelGrid.setLeafSize(1.0f, 1.0f, 1.0f); // Set the voxel grid leaf size to 1 meter

    pcl::PointCloud<pcl::PointXYZ>::Ptr cloudFiltered(new pcl::PointCloud<pcl::PointXYZ>);
    voxelGrid.filter(*cloudFiltered);

    for (const auto& point : cloudFiltered->points) {
        std::cout << point.x << " " << point.y << std::endl;
    }

    pcl::visualization::PCLVisualizer::Ptr viewer(new pcl::visualization::PCLVisualizer("Voxel Grid Visualization"));
    viewer->setBackgroundColor(0, 0, 0);

    pcl::visualization::PointCloudColorHandlerCustom<pcl::PointXYZ> originalCloudColorHandler(cloud, 255, 255, 255); // White
    viewer->addPointCloud<pcl::PointXYZ>(cloud, originalCloudColorHandler, "original cloud");

    pcl::visualization::PointCloudColorHandlerCustom<pcl::PointXYZ> filteredCloudColorHandler(cloudFiltered, 230, 20, 20); // Red
    viewer->addPointCloud<pcl::PointXYZ>(cloudFiltered, filteredCloudColorHandler, "filtered cloud");

    viewer->setPointCloudRenderingProperties(pcl::visualization::PCL_VISUALIZER_POINT_SIZE, 2, "original cloud");
    viewer->setPointCloudRenderingProperties(pcl::visualization::PCL_VISUALIZER_POINT_SIZE, 2, "filtered cloud");

    viewer->addCoordinateSystem(1.0);
    viewer->initCameraParameters();

    while (!viewer->wasStopped()) {
        viewer->spinOnce(100);
    }

    return 0;

}


